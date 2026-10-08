#!/usr/bin/env python3
"""Generates the v3 photo plates with the Gemini image model (REST, no SDK).

Reads GEMINI_API_KEY from the environment and the shot list from shots.json.

  python3 tools/gen_images.py --list-models
  python3 tools/gen_images.py --characters --model gemini-2.5-flash-image
  python3 tools/gen_images.py --shots --model gemini-2.5-flash-image [--only s02-entra]

Character sheets go to assets/photos/characters/<name>.png and are sent as
reference images with every shot that lists them, to keep faces consistent.
"""
import argparse
import base64
import json
import os
import pathlib
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
API = "https://generativelanguage.googleapis.com/v1beta"
OUT = ROOT / "assets" / "photos"


def key():
    k = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not k:
        sys.exit("GEMINI_API_KEY is not set in this session")
    return k


def call(path, body=None, tries=6):
    """POST/GET with backoff on overload (429/500/503) and read timeouts."""
    req = urllib.request.Request(f"{API}/{path}", data=json.dumps(body).encode() if body else None,
                                 headers={"x-goog-api-key": key(), "Content-Type": "application/json"})
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 503) or i == tries - 1:
                raise RuntimeError(f"{e.code}: {e.read().decode()[:400]}") from None
            reason = e.code
        except TimeoutError:
            if i == tries - 1:
                raise
            reason = "timeout"
        wait = 15 * 2 ** i
        print(f"  retry {i + 1} in {wait}s ({reason})", file=sys.stderr, flush=True)
        time.sleep(wait)


def generate(model, prompt, refs=(), aspect="16:9"):
    parts = [{"text": prompt}]
    for ref in refs:
        # Full-size PNG refs make the API fail with 500s; send a 768 px JPEG instead.
        jpg = subprocess.run(["ffmpeg", "-v", "error", "-i", str(ref), "-vf", "scale=-2:768", "-q:v", "3",
                              "-f", "image2", "-c:v", "mjpeg", "-"], capture_output=True, check=True).stdout
        parts.append({"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(jpg).decode()}})
    body = {"contents": [{"parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspect}}}
    res = call(f"models/{model}:generateContent", body)
    for cand in res.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            data = part.get("inline_data") or part.get("inlineData")
            if data:
                return base64.b64decode(data["data"])
    raise RuntimeError(f"no image returned: {json.dumps(res)[:400]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list-models", action="store_true")
    ap.add_argument("--characters", action="store_true")
    ap.add_argument("--shots", action="store_true")
    ap.add_argument("--only", default=None)
    ap.add_argument("--model", default="gemini-2.5-flash-image")
    a = ap.parse_args()

    if a.list_models:
        for m in call("models?pageSize=200").get("models", []):
            if "image" in m["name"] or "imagen" in m["name"]:
                print(m["name"], m.get("supportedGenerationMethods"))
        return

    spec = json.loads((ROOT / "shots.json").read_text())
    style = spec["style"]
    chars = OUT / "characters"
    chars.mkdir(parents=True, exist_ok=True)

    if a.characters:
        for name, desc in spec["characters"].items():
            if a.only and a.only != name:
                continue
            prompt = (f"Character reference portrait: {desc}. Front-facing, waist-up, neutral background "
                      f"of a softly blurred tapas bar. {style}")
            (chars / f"{name}.png").write_bytes(generate(a.model, prompt, aspect="3:4"))
            print("character", name)

    if a.shots:
        for shot in spec["shots"]:
            if a.only and a.only != shot["id"]:
                continue
            if not a.only and (OUT / f"{shot['id']}.jpg").exists():
                continue  # resumable: pass --only to regenerate one shot
            refs = [chars / f"{r}.png" for r in shot["refs"] if (chars / f"{r}.png").exists()]
            who = "; ".join(spec["characters"][r] for r in shot["refs"])
            prompt = f"{shot['prompt']}. {('People: ' + who + '. Keep their faces and clothes identical to the reference images. ') if who else ''}{style}"
            png = OUT / f"{shot['id']}.png"
            png.write_bytes(generate(a.model, prompt, refs))
            # Plates ship as JPEG: PNGs are over the 2 MB inline limit of the bundler.
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(png), "-q:v", "2", str(png.with_suffix(".jpg"))], check=True)
            png.unlink()
            print("shot", shot["id"])


if __name__ == "__main__":
    main()
