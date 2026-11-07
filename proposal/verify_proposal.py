"""Reproduce evidence checks and exercise the offline draft in real Chromium."""
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

from audit_sources import audit
from build_preview import build

HERE = Path(__file__).resolve().parent


def main():
    build()
    data, source_checks = audit()
    scenes = json.loads((HERE / 'voiceover_v2.json').read_text())
    original = json.loads((HERE / 'source' / 'video_plan.json').read_text())
    original_voice = (HERE / 'source' / 'voiceover.txt').read_text().strip()
    assert original_voice == '\n\n'.join(s['voiceover'] for s in original['segments'])
    pattern = r"\b[\w]+(?:[’'-][\w]+)*\b"
    original_counts = [len(re.findall(pattern, s['voiceover'])) for s in original['segments']]
    assert sum(original_counts) == 172
    revised_counts = [len(re.findall(pattern, s['voiceover'])) for s in scenes]
    revised_text = ' '.join(s['voiceover'] for s in scenes)
    # Scope exclusions apply to the new narration, not to preserved reference files.
    assert not re.search(r'\b(inflation|IPC|drift|champion|Senior|1,914)\b', revised_text, re.I)
    assert sum(r['selected'] for r in data['features']) == 1
    assert max(data['features'], key=lambda r: r['delta_auc'])['id'] == 'relative3_funds'
    (HERE / 'frames').mkdir(exist_ok=True)
    browser_errors = []
    boundary_checks = []
    layout_issues = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--disable-dev-shm-usage'])
        page = browser.new_page(viewport={'width':1920, 'height':1350}, device_scale_factor=1)
        page.on('pageerror', lambda error: browser_errors.append(str(error)))
        # file:// is blocked by managed browser policy; the self-contained page needs no origin.
        page.set_content((HERE / 'storyboard_v2.html').read_text())
        for scene in scenes:
            for t in [scene['start'], (scene['start'] + scene['end']) / 2, scene['end'] - .001]:
                actual = page.evaluate('(t) => window.renderAt(t)', t)
                assert actual == scene['id']
                assert page.locator('#narration').inner_text() == scene['voiceover']
                boundary_checks.append({'time': t, 'scene': actual})
            page.locator(f'[data-seek="{scene["start"]}"]').click()
            assert page.locator('#stage svg').get_attribute('data-scene') == scene['id']
            pose = min(scene['end'] - 1, scene['start'] + 11)
            page.evaluate('(t) => window.renderAt(t)', pose)
            # SVG coordinates, after all progressive reveals have settled.
            issues = page.evaluate('''() => [...document.querySelectorAll('#stage svg text')].map(el=>{
              const b=el.getBBox();return {text:el.textContent,x:b.x,y:b.y,w:b.width,h:b.height};
            }).filter(b=>b.x<0 || b.y<0 || b.x+b.w>1920 || b.y+b.h>940 ||
              (b.x+b.w>1630 && b.x<1830 && b.y<280 && b.y+b.h>80))''')
            layout_issues.extend({'scene': scene['id'], **issue} for issue in issues)
            svg = page.locator('#stage svg').evaluate('(el) => el.outerHTML')
            root = ET.fromstring(svg)
            assert root.attrib['viewBox'] == '0 0 1920 1080'
            (HERE / 'frames' / f'{scene["id"]}.svg').write_text(svg)
            frame_page = browser.new_page(viewport={'width':1920, 'height':1080}, device_scale_factor=1)
            frame_page.set_content('<html><body style="margin:0;width:1920px;height:1080px;overflow:hidden">'+svg+'</body></html>')
            frame_page.screenshot(path=str(HERE / 'frames' / f'{scene["id"]}.png'))
            frame_page.close()
        assert page.evaluate('window.renderAt(90)') == 'decision'
        page.locator('#headshot').check()
        assert page.locator('[data-headshot-guide]').count() == 1
        page.locator('#headshot').uncheck()
        page.evaluate('window.renderAt(27)')
        early = page.locator('#stage svg').inner_html()
        page.evaluate('window.renderAt(31)')
        assert early != page.locator('#stage svg').inner_html(), 'Within-scene reveals must change, not just whole-slide swaps'
        page.locator('[data-seek="0"]').click()
        page.locator('#play').click()
        page.wait_for_timeout(350)
        assert float(page.locator('#scrub').input_value()) > 0
        page.locator('#play').click()
        assert page.locator('#play').inner_text() == 'Play'
        browser.close()
    assert not browser_errors, browser_errors
    assert not layout_issues, layout_issues

    sheet = Image.new('RGB', (1920, 3 * 570), '#15202a')
    draw = ImageDraw.Draw(sheet)
    for i, scene in enumerate(scenes):
        with Image.open(HERE / 'frames' / f'{scene["id"]}.png') as frame:
            assert frame.size == (1920,1080)
            image = frame.resize((960,540))
        x, y = i % 2 * 960, i // 2 * 570
        sheet.paste(image, (x,y+30))
        draw.text((x+16,y+9),f'{scene["start"]:02d}–{scene["end"]:02d}s  {scene["title"]}',fill='#e8eef1')
    sheet.save(HERE / 'frames' / 'contact_sheet.jpg', quality=92)
    result = {
        'status': 'REVIEW_DRAFT_VERIFIED_WITH_SOURCE_GAPS',
        'source_reconciliation': source_checks['status'],
        'source_gaps': source_checks['source_gaps'],
        'original_voiceover_words': sum(original_counts),
        'revised_voiceover_words': sum(revised_counts),
        'revised_segment_word_counts': revised_counts,
        'revised_segment_target_wpm': [round(n / (s['end']-s['start']) * 60, 1) for n,s in zip(revised_counts,scenes)],
        'duration': '90-second edit target; recording not supplied or measured',
        'browser_scene_boundary_checks': boundary_checks,
        'browser_errors': browser_errors, 'layout_issues': layout_issues,
        'scene_navigation_checked': True, 'headshot_guide_checked': True,
        'play_pause_checked': True, 'within_scene_reveals_checked': True,
        'rendered_keyframes': 6, 'keyframe_dimensions': [1920,1080],
        'final_manim_build': 'NOT RUN', 'final_video_render': 'NOT RUN',
    }
    (HERE / 'review' / 'verification.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
