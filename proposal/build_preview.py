"""Build the offline visual draft from the reconciled data and editable scene source."""
import json
from pathlib import Path
from audit_sources import audit

HERE = Path(__file__).resolve().parent


def build():
    data, _ = audit()
    scenes = json.loads((HERE / 'voiceover_v2.json').read_text())
    assert scenes[0]['start'] == 0 and scenes[-1]['end'] == 90
    assert all(a['end'] == b['start'] for a, b in zip(scenes, scenes[1:]))
    (HERE / 'voiceover_v2.txt').write_text('\n\n'.join(s['voiceover'] for s in scenes) + '\n')
    payload = json.dumps(dict(data=data, scenes=scenes), ensure_ascii=False).replace('</', '<\\/')
    page = (HERE / 'preview_template.html').read_text()
    page = page.replace('__PAYLOAD__', payload).replace('__SCENE_SOURCE__', (HERE / 'scenes.js').read_text())
    (HERE / 'storyboard_v2.html').write_text(page)


if __name__ == '__main__':
    build()
    print('Built proposal/storyboard_v2.html and voiceover_v2.txt')
