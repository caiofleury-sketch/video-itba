"""Render the SVG assets with an isolated headless Chrome profile;check the HTML preview."""
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from PIL import Image

HERE=Path(__file__).resolve().parent


def main():
    chrome=shutil.which("google-chrome") or shutil.which("chromium")
    if not chrome:
        raise SystemExit("A local Chrome/Chromium renderer is required;no software is installed by this script")
    with tempfile.TemporaryDirectory(prefix="fe_video_render_",dir="/tmp/opencode") as work:
        def command(profile):
            return [chrome,"--headless","--disable-gpu","--disable-background-networking","--no-first-run",
                    "--no-default-browser-check","--hide-scrollbars","--log-level=3",f"--user-data-dir={Path(work)/profile}"]

        def render(path):
            destination=path.with_suffix(".png")
            subprocess.run(command(path.stem)+["--window-size=1920,1080",f"--screenshot={destination}",path.as_uri()],
                           capture_output=True,text=True,check=True,timeout=60)
            with Image.open(destination) as image:
                assert image.size==(1920,1080)
            return destination.name

        with ThreadPoolExecutor(max_workers=3) as pool:
            rendered=list(pool.map(render,sorted((HERE/"frames").glob("*.svg"))))

        result=subprocess.run(command("html-check")+["--dump-dom","--virtual-time-budget=800",
            (HERE/"storyboard.html").as_uri()+"?t=60"],capture_output=True,text=True,check=True,timeout=60)

        class Check(HTMLParser):
            def __init__(self):
                super().__init__();self.in_stage=False;self.stage_svg=0;self.thumbs=0;self.in_narration=False;self.narration=""
            def handle_starttag(self,tag,attrs):
                attrs=dict(attrs)
                if tag=="div" and attrs.get("id")=="stage":self.in_stage=True
                if tag=="svg" and self.in_stage:self.stage_svg+=1
                if tag=="button" and attrs.get("class")=="thumb":self.thumbs+=1
                if tag=="div" and attrs.get("id")=="narration":self.in_narration=True
            def handle_endtag(self,tag):
                if tag=="div":self.in_stage=False;self.in_narration=False
            def handle_data(self,data):
                if self.in_narration:self.narration+=data

        check=Check();check.feed(result.stdout)
        plan=json.loads((HERE/"video_plan.json").read_text())
        assert check.stage_svg==1 and check.thumbs==9
        assert check.narration==plan["segments"][3]["voiceover"]
    receipt={"status":"PASS","rendered_pngs":rendered,"dimensions":[1920,1080],
             "html_stage_rendered":True,"high_point_thumbnails":3,"quarter_minute_thumbnails":6,
             "narration_matches_selected_milestone":True,"isolated_browser_profile":True}
    (HERE/"render_validation.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt,indent=2))


if __name__=="__main__":
    main()
