"""Render a deterministic, silent browser animatic; not a Manim production render."""
import base64
import json
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright
from build import build

HERE=Path(__file__).resolve().parent
FPS=24


def main():
    data=build()
    output=HERE/'animatic_120s.mp4'
    frames=FPS*data['duration']
    with (HERE/'render.log').open('w') as log:
        process=subprocess.Popen([
            'ffmpeg','-hide_banner','-loglevel','error','-y',
            '-f','image2pipe','-vcodec','mjpeg','-framerate',str(FPS),'-i','pipe:0',
            '-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',
            '-threads','2','-movflags','+faststart',str(output)
        ],stdin=subprocess.PIPE,stderr=log)
        try:
            with sync_playwright() as p:
                browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--disable-dev-shm-usage'])
                page=browser.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1)
                page.set_content((HERE/'index.html').read_text())
                page.add_style_tag(content='''main{max-width:none!important;padding:0!important}header,.controls,nav,#narration,.note,details{display:none!important}.stage{width:1920px!important;height:1080px!important;border:none!important}''')
                page.evaluate('document.fonts.ready')
                cdp=page.context.new_cdp_session(page)
                for i in range(frames):
                    page.evaluate('(t)=>window.renderAt(t)',i/FPS)
                    shot=cdp.send('Page.captureScreenshot',{'format':'jpeg','quality':95,'fromSurface':True,'captureBeyondViewport':False})
                    process.stdin.write(base64.b64decode(shot['data']))
                    if i%240==0:print(f'Rendered {i}/{frames} frames ({i/FPS:.0f}/{data["duration"]} seconds)',flush=True)
                browser.close()
            process.stdin.close()
            returncode=process.wait()
            if returncode:raise RuntimeError(f'ffmpeg failed with exit {returncode}; see render.log')
        except BaseException:
            if process.poll() is None:process.terminate()
            process.wait()
            raise
    result=json.loads(subprocess.check_output([
        'ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,codec_type,width,height,r_frame_rate,nb_frames',
        '-of','json',str(output)
    ],text=True))
    stream=result['streams'][0]
    assert len(result['streams'])==1 and stream['codec_type']=='video'
    assert (stream['width'],stream['height'])==(1920,1080)
    assert stream['r_frame_rate']==f'{FPS}/1' and int(stream['nb_frames'])==frames
    assert abs(float(result['format']['duration'])-data['duration'])<.05
    (HERE/'render_verification.json').write_text(json.dumps(dict(
        status='SILENT_BROWSER_ANIMATIC_RENDERED',engine='Chromium SVG + FFmpeg, not Manim',
        illustrative_opening=True,audio=False,frames=frames,fps=FPS,duration_seconds=data['duration'],
        dimensions=[1920,1080],output=str(output),ffprobe=result,
    ),indent=2)+'\n')
    print(f'Complete: {output}',flush=True)


if __name__=='__main__':main()
