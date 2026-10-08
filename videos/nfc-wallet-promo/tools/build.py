#!/usr/bin/env python3
"""Generates the NFC Wallet promo compositions (16:9 master).

Writes compositions/sNN.html (one sub-composition per storyboard frame) and
index.html (slots, leftward push/whip transitions and the Lyria music bed;
v3 has no voice-over and no SFX). Run from the project root: python3 tools/build.py
"""
import html
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
W, H = 1920, 1080

# Scene boundaries snapped to the strongest beat within ±0.35 s of the v2 cuts,
# on assets/music/lyria.wav (see beats/).
B = [0, 5.767, 14.339, 23.812, 32.835, 41.857, 48.173, 61.707, 69.827, 79.978, 83.587, 94.414, 103.887, 113.136, 123.512, 135]
# Transition INTO each scene: (kind, overlap seconds).
TIN = {1: ("none", 0), 2: ("push", .35), 3: ("cut", 0), 4: ("cut", 0), 5: ("push", .35),
       6: ("cut", 0), 7: ("push", .35), 8: ("whip", .25), 9: ("push", .35), 10: ("cut", 0),
       11: ("push", .35), 12: ("push", .35), 13: ("push", .35), 14: ("push", .35), 15: ("whip", .25)}
TOTAL = B[-1]


def slot(n):
    """(start, duration, overlap) of scene n in root time."""
    ov = TIN[n][1]
    start = B[n - 1] - ov
    return round(start, 3), round(B[n] - start, 3), ov


def wav_len(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return float(out.stdout.strip())


# ---------------------------------------------------------------- shared look
FONTS = """
@font-face { font-family: "Archivo Black"; src: url("assets/fonts/archivo-black-400.woff2") format("woff2"); font-weight: 400; }
@font-face { font-family: "Montserrat"; src: url("assets/fonts/montserrat-var.woff2") format("woff2"); font-weight: 100 900; }
"""

PHOTO_CSS = """
.nw-ph { position: absolute; inset: 0; overflow: hidden; }
.nw-scrim { position: absolute; inset: 0; pointer-events: none; }
.nw-ink.nw-ink { color: #FBF5EC; }
.nw-ink .nw-blue, .nw-blue-l { color: #8FB0FF; }
.nw-ph img { position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; transform-origin: 50% 50%; }
"""

SHARED_CSS = FONTS + PHOTO_CSS + """
.nw-h { font-family: "Archivo Black", sans-serif; font-weight: 400; line-height: .92; letter-spacing: -.01em; margin: 0; }
.nw-blue { color: #1F5EFF; }
.nw-abs { position: absolute; }
.nw-ghost { position: absolute; font-family: "Archivo Black", sans-serif; color: #141A33; opacity: .07; white-space: nowrap; line-height: .8; }
.nw-glow { position: absolute; border-radius: 50%; background: radial-gradient(circle, rgba(31,94,255,.26), rgba(31,94,255,0) 68%); }
.nw-meta { position: absolute; font-family: "Montserrat", sans-serif; font-size: 24px; font-weight: 800; letter-spacing: .18em; text-transform: uppercase; color: #5B6178; }
.nw-phone { position: absolute; width: 380px; height: 800px; background: #0E1222; border-radius: 64px; padding: 16px; box-shadow: 0 40px 80px rgba(20,26,51,.28); }
.nw-screen { position: relative; width: 100%; height: 100%; border-radius: 50px; overflow: hidden; background: #1F2937; }
.nw-notch { position: absolute; left: 50%; top: 16px; width: 110px; height: 30px; margin-left: -55px; background: #0E1222; border-radius: 20px; z-index: 5; }
.nw-pass { position: absolute; border-radius: 30px; background: #1F2937; color: #fff; padding: 34px 38px; box-shadow: 0 30px 60px rgba(20,26,51,.30); font-family: "Montserrat", sans-serif; }
.nw-pass .row { display: flex; align-items: center; gap: 18px; }
.nw-pass .name { font-family: "Archivo Black", sans-serif; font-size: 34px; }
.nw-pass .lbl { font-size: 18px; font-weight: 700; opacity: .72; text-transform: uppercase; letter-spacing: .14em; margin-top: 22px; }
.nw-pass .val { font-size: 46px; font-weight: 800; }
.nw-stamps { display: flex; gap: 14px; margin-top: 12px; }
.nw-stamps i { display: block; width: 52px; height: 52px; border-radius: 50%; border: 5px solid rgba(255,255,255,.45); }
.nw-stamps i b { display: block; width: 100%; height: 100%; border-radius: 50%; background: #F4A12B; opacity: 0; }
.nw-stamps i b.on { opacity: 1; }
.nw-logo { width: 64px; height: 64px; border-radius: 50%; background: #F4A12B; color: #1F2937; display: grid; place-items: center; font-family: "Archivo Black", sans-serif; font-size: 34px; flex: none; }
.nw-btn { display: inline-block; border-radius: 999px; padding: 18px 36px; font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 26px; background: #000; color: #fff; }
.nw-panel { position: absolute; background: #fff; border-radius: 28px; border: 3px solid #E3E6EB; box-shadow: 0 40px 80px rgba(20,26,51,.18); overflow: hidden; font-family: "Montserrat", sans-serif; color: #141A33; }
.nw-panel .bar { height: 64px; background: #F6F7F9; border-bottom: 3px solid #E3E6EB; display: flex; align-items: center; gap: 12px; padding: 0 26px; font-size: 22px; font-weight: 800; }
.nw-panel .bar i { display: block; width: 16px; height: 16px; border-radius: 50%; background: #D6D9E0; }
.nw-field { border: 3px solid #E3E6EB; border-radius: 16px; padding: 18px 22px; font-size: 30px; font-weight: 600; background: #fff; }
.nw-num { position: absolute; width: 70px; height: 70px; border-radius: 50%; background: #1F5EFF; color: #fff; font-family: "Archivo Black", sans-serif; font-size: 38px; display: grid; place-items: center; box-shadow: 0 0 0 12px rgba(31,94,255,.18); }
.nw-cursor { position: absolute; width: 56px; height: 56px; }
.nw-notif { position: absolute; background: rgba(255,255,255,.95); border-radius: 30px; padding: 24px 28px; box-shadow: 0 20px 50px rgba(0,0,0,.28); display: flex; gap: 20px; align-items: center; font-family: "Montserrat", sans-serif; color: #141A33; }
.nw-notif .t1 { font-size: 22px; font-weight: 800; letter-spacing: .06em; text-transform: uppercase; color: #5B6178; }
.nw-notif .t2 { font-size: 30px; font-weight: 700; }
.nw-chip { display: inline-block; border-radius: 999px; padding: 12px 26px; font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 28px; }
"""

CURSOR_SVG = ('<svg viewBox="0 0 24 24"><path d="M4 2 L20 13 L12.5 14.2 L16.6 22 L13.4 23.4 L9.4 15.6 L4 20 Z" '
              'fill="#141A33" stroke="#fff" stroke-width="1.4" stroke-linejoin="round"/></svg>')

BEER_SVG = ('<svg viewBox="0 0 40 40" width="{s}" height="{s}"><rect x="8" y="10" width="20" height="26" rx="3" fill="#F4A12B"/>'
            '<path d="M8 10 q0-6 10-6 q10 0 10 6z" fill="#fff"/><path d="M28 16 h4 q4 0 4 5 v3 q0 5-4 5 h-4" '
            'fill="none" stroke="#F4A12B" stroke-width="3"/></svg>')


def pass_card(pid, stamps_on=0, w=600, extra="", reward="Café gratis", bg="#1F2937", top_label=""):
    stamps = "".join(f'<i><b class="{"on" if i < stamps_on else ""}"></b></i>' for i in range(5))
    tl = f'<div style="font-size:18px;font-weight:800;letter-spacing:.16em;opacity:.7;margin-bottom:14px">{top_label}</div>' if top_label else ""
    return f"""<div class="nw-pass" id="{pid}" style="width:{w}px;background:{bg}">
  {tl}<div class="row"><div class="nw-logo">P</div><div class="name">Restaurante Pepito</div></div>
  <div class="lbl">Sellos</div><div class="nw-stamps">{stamps}</div>
  <div class="lbl">Premio</div><div class="val" style="font-size:36px">{reward}</div>{extra}
</div>"""


def landing_screen(sid, btn_id=None):
    btn = f'id="{btn_id}"' if btn_id else ""
    return f"""<div class="nw-screen" id="{sid}" style="display:flex;flex-direction:column;align-items:center;padding:110px 34px 0;gap:22px;text-align:center;color:#fff;font-family:Montserrat,sans-serif">
  <div class="nw-logo" style="width:120px;height:120px;font-size:62px">P</div>
  <div class="nw-h" style="font-size:40px;line-height:1">Restaurante Pepito</div>
  <div style="font-size:22px;font-weight:600;opacity:.82;line-height:1.35">Guarda nuestra tarjeta en tu móvil: acumula visitas y recibe nuestras novedades.</div>
  <div style="width:100%;text-align:left;font-size:18px;font-weight:700;opacity:.8;margin-top:10px">Email (opcional)</div>
  <div style="width:100%;height:58px;border-radius:12px;background:#fff;opacity:.92"></div>
  <span class="nw-btn" {btn} style="width:100%;margin-top:14px;font-size:24px;padding:20px 0;border:2px solid rgba(255,255,255,.35)">Añadir a Apple Wallet</span>
</div>"""


def ICON(name, color="#1F5EFF", size=84):
    paths = {
        "pin": '<path d="M24 4c-8 0-14 6-14 14 0 11 14 26 14 26s14-15 14-26c0-8-6-14-14-14z" fill="C"/><circle cx="24" cy="18" r="5" fill="#fff"/>',
        "chart": '<rect x="6" y="26" width="8" height="16" rx="2" fill="C" class="bar1"/><rect x="20" y="16" width="8" height="26" rx="2" fill="C" class="bar2"/><rect x="34" y="8" width="8" height="34" rx="2" fill="C" class="bar3"/>',
        "store": '<path d="M6 18 L10 6 H38 L42 18 Z" fill="C"/><rect x="9" y="18" width="30" height="22" fill="C" opacity=".55"/><rect x="20" y="27" width="8" height="13" fill="#fff"/>',
        "lock": '<rect x="9" y="20" width="30" height="22" rx="5" fill="C"/><path d="M15 20 v-6 a9 9 0 0 1 18 0 v6" fill="none" stroke="C" stroke-width="5"/><circle cx="24" cy="31" r="4" fill="#fff"/>',
        "receipt": '<path d="M10 4 H38 V44 L33 40 L28 44 L24 40 L20 44 L15 40 L10 44 Z" fill="C"/><path d="M16 14 H32 M16 22 H32 M16 30 H26" stroke="#fff" stroke-width="3.4" stroke-linecap="round"/>',
        "shield": '<path d="M24 4 L40 10 V22 C40 33 33 40 24 44 C15 40 8 33 8 22 V10 Z" fill="C"/><path d="M17 24 l5 5 l10 -11" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
    }[name].replace('"C"', f'"{color}"')
    return f'<svg viewBox="0 0 48 48" width="{size}" height="{size}">{paths}</svg>'


def NFC_WAVES(color="#fff", size=60, sw=6):
    return (f'<svg viewBox="0 0 48 48" width="{size}" height="{size}"><g fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round">'
            '<path d="M14 16 a12 12 0 0 1 0 16"/><path d="M22 10 a20 20 0 0 1 0 28"/><path d="M30 4 a28 28 0 0 1 0 40"/></g></svg>')


def scene(sid, n, body, css, js):
    """Wraps a scene: template transport, scoped CSS, one paused timeline."""
    start, dur, ov = slot(n)
    return f"""<!doctype html>
<html lang="es">
<head><meta charset="UTF-8" /></head>
<body>
<template>
<style>
{SHARED_CSS}
#{sid}, #{sid} * {{ box-sizing: border-box; }}
#{sid} {{ position: absolute; inset: 0; overflow: hidden; background: #FBF5EC; color: #141A33; font-family: "Montserrat", sans-serif; }}
{css}
</style>
<div id="{sid}" data-composition-id="{sid}" data-width="{W}" data-height="{H}" data-duration="{dur}">
{body}
</div>
<script>
(() => {{
  const D = {dur};      // slot length (s)
  const IN = {ov};      // incoming transition overlap (s): content should be readable from here
  const S = (q) => "#{sid} " + q;
  const tl = gsap.timeline({{ paused: true }});
  const breath = (sel, at, cycle, props) => {{
    const len = Math.max(0, D - at);
    tl.to(S(sel), Object.assign({{ duration: cycle / 2, ease: "sine.inOut", yoyo: true,
      repeat: Math.max(0, Math.floor(len / cycle) * 2 - 1) }}, props), at);
  }};
  const typeText = (sel, text, at, dur) => {{
    const el = document.querySelector(S(sel));
    const st = {{ n: 0 }};
    tl.fromTo(st, {{ n: 0 }}, {{ n: text.length, duration: dur, ease: "none",
      onUpdate: () => {{ el.textContent = text.slice(0, Math.round(st.n)); }} }}, at);
  }};
  const countUp = (sel, to, at, dur, fmt) => {{
    const el = document.querySelector(S(sel));
    const st = {{ v: 0 }};
    tl.fromTo(st, {{ v: 0 }}, {{ v: to, duration: dur, ease: "power2.out",
      onUpdate: () => {{ el.textContent = (fmt || String)(Math.round(st.v)); }} }}, at);
  }};
{js}
  window.__timelines["{sid}"] = tl;
}})();
</script>
</template>
</body>
</html>
"""


# ---------------------------------------------------------------- v3 photo plates (helpers)
# Photorealistic plates generated with Gemini (tools/gen_images.py, shots.json).
# photo(): one full-frame layer per shot, stacked in order; each later shot hard-cuts
# in at its start time. Ken Burns: (scale0, x0, y0) -> (scale1, x1, y1) over the shot.


def photo(sid, shots, box="inset:0", radius=0):
    """shots: [(shot_id, start, (s0, x0, y0), (s1, x1, y1))]. Returns (body, js)."""
    layers, js = [], []
    for i, (shot, t0, a, b) in enumerate(shots):
        lid = f"{sid}-ph{i}"
        layers.append(f'<div class="nw-ph" id="{lid}" style="opacity:{1 if i == 0 else 0}">'
                      f'<img src="assets/photos/{shot}.jpg" alt="" /></div>')
        t1 = shots[i + 1][1] if i + 1 < len(shots) else None
        js.append(f'  tl.fromTo(S("#{lid} img"), {{ scale: {a[0]}, x: {a[1]}, y: {a[2]} }}, '
                  f'{{ scale: {b[0]}, x: {b[1]}, y: {b[2]}, duration: {f"{t1} - {t0}" if t1 is not None else f"D - {t0}"}, ease: "none" }}, {t0});')
        if i:
            js.append(f'  tl.set(S("#{lid}"), {{ opacity: 1 }}, {t0});')
    body = (f'<div class="nw-abs" id="{sid}-photo" style="{box};overflow:hidden;border-radius:{radius}px">'
            + "".join(layers) + "</div>")
    return body, "\n".join(js) + "\n"


SCENES = {}

# ---------------------------------------------------------------- 01 hook
SCENES[1] = dict(
    body=f"""
<div class="nw-glow" id="s01-glow" style="width:1200px;height:1200px;right:-300px;top:-420px"></div>
<div class="nw-ghost" id="s01-ghost" style="font-size:560px;left:-60px;bottom:-110px">SOLOS</div>
<div class="nw-meta" style="left:120px;top:110px">NFC Wallet · para bares y restaurantes</div>
<div class="nw-abs" id="s01-rule" style="left:120px;top:170px;width:220px;height:8px;background:#1F5EFF;transform-origin:0 50%"></div>
<p class="nw-h nw-abs" id="s01-l1" style="left:120px;top:250px;font-size:132px">¿Y si tus clientes</p>
<p class="nw-h nw-abs" id="s01-l2" style="left:120px;top:400px;font-size:132px">volvieran</p>
<p class="nw-h nw-abs nw-blue" id="s01-l3" style="left:112px;top:560px;font-size:330px;transform-origin:0 70%">SOLOS?</p>
""",
    css="",
    js="""
  tl.fromTo(S("#s01-rule"), { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: "expo.out" }, 0.05);
  tl.fromTo(S("#s01-l1"), { scale: 1.35, filter: "blur(14px)", opacity: 0, transformOrigin: "0% 50%" },
    { scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.45, ease: "power4.out" }, 0.12);
  tl.fromTo(S("#s01-l2"), { x: -260, opacity: 0 }, { x: 0, opacity: 1, duration: 0.42, ease: "expo.out" }, 0.78);
  tl.fromTo(S("#s01-l3"), { scale: 1.7, y: 60, rotation: -4, opacity: 0 },
    { scale: 1, y: 0, rotation: 0, opacity: 1, duration: 0.55, ease: "circ.out" }, 1.42);
  tl.fromTo(S("#s01-ghost"), { x: 0 }, { x: -220, duration: D, ease: "none" }, 0);
  breath("#s01-glow", 0, 2.4, { scale: 1.12 });
  breath("#s01-l3", 2.1, 1.7, { scale: 1.025 });
""")

# ---------------------------------------------------------------- 02 arrive
S02_PH = photo("s02", [("s02-entra", 0, (1.08, 0, 0), (1.2, -40, 10)),
                       ("s02-sienta", 4.4, (1.16, 60, 0), (1.05, 0, 0))])
SCENES[2] = dict(
    body=S02_PH[0] + """
<div class="nw-scrim" style="background:linear-gradient(to top, rgba(14,18,34,.82) 0%, rgba(14,18,34,0) 46%), linear-gradient(to bottom, rgba(14,18,34,.55) 0%, rgba(14,18,34,0) 22%)"></div>
<div class="nw-meta nw-ink" style="left:120px;top:70px" id="s02-tag">Restaurante Pepito · 14:05</div>
<p class="nw-h nw-abs nw-ink" id="s02-h1" style="left:120px;top:800px;font-size:110px;white-space:nowrap">Lucía entra en <span class="nw-blue">Pepito.</span></p>
<p class="nw-h nw-abs nw-ink" id="s02-h2" style="left:120px;top:800px;font-size:110px;white-space:nowrap">Deja el móvil <span class="nw-blue">en la mesa.</span></p>
""",
    css="",
    js=S02_PH[1] + """
  tl.fromTo(S("#s02-tag"), { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, IN);
  tl.fromTo(S("#s02-h1"), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "power4.out" }, 0.6);
  tl.to(S("#s02-h1"), { y: -40, opacity: 0, duration: 0.25, ease: "power2.in" }, 4.15);
  tl.fromTo(S("#s02-h2"), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "power4.out" }, 4.55);
""")

# ---------------------------------------------------------------- 03 tap
S03_PH = photo("s03", [("s03-mesa", 0, (1.05, 0, 0), (1.18, -30, 20))])
SCENES[3] = dict(
    body=S03_PH[0] + """<div class="nw-scrim" id="s03-scrim" style="background:rgba(14,18,34,.58)"></div>""" + f"""
<div class="nw-abs" id="s03-tag" style="left:250px;top:330px;width:420px;height:420px;border-radius:52px;background:#FBF5EC;box-shadow:0 30px 60px rgba(60,30,10,.35);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px">
  <div style="color:#1F5EFF">{NFC_WAVES("#1F5EFF", 90, 6)}</div>
  <div class="nw-h" style="font-size:66px;text-align:center;line-height:.95">TOCA<br>AQUÍ</div>
  <div style="font-weight:800;font-size:24px;color:#1F5EFF;letter-spacing:.12em">NFC · MESA 4</div>
</div>
<div class="nw-abs" id="s03-waves" style="left:300px;top:380px;width:320px;height:320px">
  <div class="s03-ring" style="--d:0"></div><div class="s03-ring"></div><div class="s03-ring"></div>
</div>
<div class="nw-phone" id="s03-phone" style="left:760px;top:140px">
  <div class="nw-notch"></div>
  <div class="nw-screen" id="s03-off" style="background:#0B0F1C"></div>
  <div class="nw-abs" id="s03-on" style="left:16px;top:16px;right:16px;bottom:16px">{landing_screen("s03-landing")}</div>
</div>
<p class="nw-h nw-abs" id="s03-title" style="right:120px;top:300px;font-size:150px;text-align:right;color:#FBF5EC;line-height:.9">Un<br>toque.</p>
<div class="nw-abs" id="s03-chips" style="right:120px;top:640px;display:flex;flex-direction:column;align-items:flex-end;gap:18px">
  <span class="nw-chip" id="s03-c1" style="background:#FBF5EC;color:#141A33">Sin descargar apps</span>
  <span class="nw-chip" id="s03-c2" style="background:#1F5EFF;color:#fff">Sin códigos QR</span>
</div>
""",
    css="""
#s03 .s03-ring { position: absolute; inset: 0; border-radius: 50%; border: 8px solid #FBF5EC; opacity: 0; }
#s03-on { overflow: hidden; border-radius: 50px; }
""",
    js=S03_PH[1] + """
  tl.fromTo(S("#s03-scrim"), { opacity: 0.25 }, { opacity: 1, duration: 0.8, ease: "power2.out" }, 0.4);
  tl.fromTo(S("#s03-tag"), { scale: 0.85, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: "power3.out" }, 0.05);
  tl.fromTo(S("#s03-phone"), { x: 420, y: -820, rotation: 22 }, { x: 0, y: 0, rotation: -6, duration: 1.0, ease: "power3.inOut" }, 0.9);
  // Tap: the phone dips onto the tag, rings radiate, the screen wakes.
  tl.to(S("#s03-phone"), { x: -330, y: 60, rotation: -10, duration: 0.45, ease: "power3.in" }, 2.15);
  tl.to(S("#s03-phone"), { x: 0, y: 0, rotation: -6, duration: 0.6, ease: "power3.out" }, 2.75);
  gsap.utils.toArray(S(".s03-ring")).forEach((r, i) => {
    tl.fromTo(r, { scale: 0.4, opacity: 0.9 }, { scale: 1.9, opacity: 0, duration: 0.9, ease: "power2.out" }, 2.55 + i * 0.18);
  });
  tl.fromTo(S("#s03-on"), { opacity: 0 }, { opacity: 1, duration: 0.25, ease: "power1.out" }, 2.8);
  tl.fromTo(S("#s03-landing > *"), { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "power3.out", stagger: 0.07 }, 3.0);
  tl.fromTo(S("#s03-title"), { x: 120, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: "expo.out" }, 2.6);
  tl.fromTo(S("#s03-c1"), { x: 80, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 5.6);
  tl.fromTo(S("#s03-c2"), { x: 80, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 6.1);
  breath("#s03-phone", 3.6, 2.2, { y: -12 });
""")

# ---------------------------------------------------------------- 04 wallet
S04_PASS = pass_card("s04-pass", 0, 640, extra='<div class="lbl">Muéstrala al camarero</div><div class="s04-qr"></div>')
SCENES[4] = dict(
    body=f"""
<div class="nw-glow" id="s04-glow" style="width:1100px;height:1100px;left:420px;top:-200px"></div>
<div class="nw-phone" id="s04-phone" style="left:200px;top:140px">
  <div class="nw-notch"></div>
  {landing_screen("s04-landing", "s04-btn")}
  <div class="nw-abs" id="s04-wallet" data-layout-allow-overlap data-layout-allow-occlusion style="left:16px;top:16px;right:16px;bottom:16px;border-radius:50px;background:#0B0F1C;overflow:hidden">
    <div style="color:#fff;font-family:Montserrat;font-weight:800;font-size:34px;padding:90px 30px 20px">Wallet</div>
    <div style="margin:0 22px;height:200px;border-radius:22px;background:#1F2937;padding:22px;display:flex;gap:14px;align-items:center;color:#fff"><div class="nw-logo">P</div><div class="nw-h" style="font-size:26px">Restaurante Pepito</div></div>
    <div style="margin:-150px 22px 0;height:200px;border-radius:22px;background:#3A4560;opacity:.6;transform:translateY(190px)"></div>
  </div>
</div>
<div class="nw-abs" id="s04-ring" style="left:274px;top:776px;width:232px;height:84px;border-radius:999px;border:6px solid #1F5EFF"></div>
<div class="nw-abs" id="s04-passwrap" style="left:760px;top:150px">{S04_PASS}</div>
<div class="nw-abs" style="left:760px;top:800px;width:1040px">
  <p class="nw-h" style="font-size:96px"><span id="s04-w1" style="display:inline-block">Sin apps.</span> <span id="s04-w2" class="nw-blue" style="display:inline-block">Sin registros.</span></p>
</div>
""",
    css="""
#s04-passwrap .nw-pass { position: relative; }
#s04 .s04-qr { width: 150px; height: 150px; margin-top: 14px; border-radius: 12px; border: 10px solid #fff;
  background: conic-gradient(from 90deg at 50% 50%, #fff 25%, #0E1222 0 50%, #fff 0 75%, #0E1222 0) 0 0 / 32px 32px; }
""",
    js="""
  tl.fromTo(S("#s04-phone"), { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 0);
  tl.fromTo(S("#s04-ring"), { scale: 0.7, opacity: 0 }, { scale: 1.15, opacity: 1, duration: 0.3, ease: "power2.out" }, 1.05);
  tl.to(S("#s04-ring"), { scale: 1.45, opacity: 0, duration: 0.35, ease: "power2.out" }, 1.35);
  tl.fromTo(S("#s04-btn"), { scale: 1 }, { scale: 0.93, duration: 0.12, ease: "power2.out", yoyo: true, repeat: 1 }, 1.1);
  tl.fromTo(S("#s04-wallet"), { yPercent: 100 }, { yPercent: 0, duration: 0.5, ease: "expo.out" }, 1.5);
  tl.fromTo(S("#s04-landing"), { opacity: 1 }, { opacity: 0, duration: 0.3, ease: "power1.out" }, 1.55);
  // The card flies out of the phone and parks on the right.
  tl.fromTo(S("#s04-passwrap"), { x: -520, y: 260, scale: 0.35, rotation: -12, opacity: 0 },
    { x: 0, y: 0, scale: 1, rotation: 0, opacity: 1, duration: 0.75, ease: "expo.out" }, 1.75);
  tl.fromTo(S("#s04-w1"), { y: 70, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power4.out" }, 2.05);
  tl.fromTo(S("#s04-w2"), { x: 160, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "expo.out" }, 2.65);
  breath("#s04-glow", 0, 2.6, { scale: 1.1 });
  breath("#s04-passwrap", 3.2, 2.4, { y: -12 });
""")

# ---------------------------------------------------------------- 05 eats & leaves
S05_PH = photo("s05", [("s05-come", 0, (1.06, 0, 0), (1.16, 20, -10)),
                       ("s05-sale", 2.8, (1.14, -30, 0), (1.04, 0, 0))],
               box="left:860px;top:130px;width:940px;height:820px", radius=30)
SCENES[5] = dict(
    body=f"""
<div class="nw-abs" id="s05-passwrap" style="left:120px;top:150px">{pass_card("s05-pass", 0, 600)}</div>
<p class="nw-h nw-abs nw-blue" id="s05-title" style="left:120px;top:730px;font-size:92px;white-space:nowrap">Primer sello.</p>
""" + S05_PH[0] + """
<p class="nw-abs" id="s05-sub" style="left:126px;top:850px;font-size:48px;font-weight:700;color:#5B6178">Come, paga… y se va.</p>
""",
    css="""
#s05-photo { box-shadow: 0 30px 60px rgba(20,26,51,.22); }
#s05-passwrap .nw-pass { position: relative; }
""",
    js="""
  tl.fromTo(S("#s05-passwrap"), { x: -60, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 0.1);
  tl.fromTo(S("#s05-pass .nw-stamps i:first-child b"), { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2.2)" }, 0.6);
  tl.fromTo(S("#s05-title"), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.42, ease: "power4.out" }, 0.75);
  tl.fromTo(S("#s05-photo"), { x: 120, opacity: 0 }, { x: 0, opacity: 1, duration: 0.5, ease: "expo.out" }, 0.2);
  tl.fromTo(S("#s05-sub"), { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 2.9);
""")

# ---------------------------------------------------------------- 06 time passes
SCENES[6] = dict(
    body="""
<div class="nw-ghost" id="s06-ghost" style="font-size:520px;right:-120px;top:20px">DÍAS</div>
<div class="nw-abs" id="s06-cal" style="left:170px;top:220px;width:520px;height:620px;background:#fff;border-radius:40px;box-shadow:0 40px 80px rgba(20,26,51,.18);overflow:hidden;text-align:center">
  <div style="background:#1F5EFF;color:#fff;font-weight:800;font-size:44px;letter-spacing:.12em;padding:28px 0">OCTUBRE</div>
  <div class="nw-h" id="s06-day" style="font-size:340px;margin-top:40px;line-height:1">3</div>
</div>
<div class="nw-abs" id="s06-sheet" style="left:170px;top:340px;width:520px;height:500px;background:#fff;border-radius:0 0 40px 40px;transform-origin:50% 0"></div>
<p class="nw-h nw-abs" id="s06-a" style="left:820px;top:330px;font-size:170px">3 semanas</p>
<p class="nw-h nw-abs nw-blue" id="s06-b" style="left:820px;top:510px;font-size:170px">después</p>
""",
    css="",
    js="""
  tl.fromTo(S("#s06-cal"), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }, 0);
  // Pages fly faster and faster: 3 → 24.
  const days = [4, 6, 8, 10, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24];
  const el = document.querySelector(S("#s06-day"));
  const flips = [];
  let t = 0.35, step = 0.26;
  days.forEach(() => {
    tl.fromTo(S("#s06-sheet"), { rotationX: 0, opacity: 0.9 }, { rotationX: -95, opacity: 0, duration: step * 0.9, ease: "power2.in", immediateRender: false }, t);
    flips.push(t + step * 0.5);
    t += step; step = Math.max(0.1, step * 0.88);
  });
  // The day number is a pure function of time (seek-safe).
  const clock = { t: 0 };
  tl.fromTo(clock, { t: 0 }, { t: 3, duration: 3, ease: "none", onUpdate: () => {
    let d = 3;
    flips.forEach((ft, i) => { if (clock.t >= ft) d = days[i]; });
    el.textContent = String(d);
  } }, 0);
  tl.fromTo(S("#s06-a"), { scale: 1.4, filter: "blur(12px)", opacity: 0, transformOrigin: "0% 50%" }, { scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.4, ease: "power4.out" }, 2.5);
  tl.fromTo(S("#s06-b"), { x: -200, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "expo.out" }, 2.85);
  tl.fromTo(S("#s06-ghost"), { x: 0 }, { x: -260, duration: D, ease: "none" }, 0);
""")

# ---------------------------------------------------------------- 07 owner sends a promo
S07_PH = photo("s07", [("s07-paco", 0, (1.04, 0, 0), (1.18, 60, -20))])
SCENES[7] = dict(
    body=S07_PH[0] + f"""
<div class="nw-scrim" id="s07-scrim" style="background:rgba(14,18,34,.62)"></div>
<div class="nw-scrim" id="s07-low" style="background:linear-gradient(to top, rgba(14,18,34,.8) 0%, rgba(14,18,34,0) 40%)"></div>
<p class="nw-h nw-abs nw-ink" id="s07-intro" style="left:120px;top:800px;font-size:110px;white-space:nowrap">Paco manda <span class="nw-blue">una promo.</span></p>
<div class="nw-panel" id="s07-panel" style="left:110px;top:120px;width:1140px;height:760px">
  <div class="bar"><i></i><i></i><i></i><span style="margin-left:16px">NFC Wallet · Restaurante Pepito · Mensajes</span></div>
  <div style="padding:44px 48px;display:flex;flex-direction:column;gap:30px">
    <div style="font-size:22px;font-weight:800;color:#5B6178;letter-spacing:.14em">NUEVO MENSAJE</div>
    <div class="nw-field" style="height:86px"><span id="s07-text"></span><span id="s07-caret" style="display:inline-block;width:3px;height:34px;background:#1F5EFF;vertical-align:-6px;margin-left:2px"></span></div>
    <div style="font-size:22px;font-weight:800;color:#5B6178;letter-spacing:.14em">AUDIENCIA</div>
    <div style="display:flex;gap:18px">
      <span class="nw-field" id="s07-all" style="font-size:26px">Todos los clientes</span>
      <span class="nw-field" style="font-size:26px;color:#5B6178">Con premio pendiente</span>
    </div>
    <div style="display:flex;align-items:center;gap:26px;margin-top:10px">
      <span class="nw-btn" id="s07-send" style="background:#1F5EFF;font-size:30px;padding:20px 56px">Enviar</span>
      <span id="s07-sent" style="font-weight:800;font-size:30px;color:#1B7F3B">✓ Enviado a <span id="s07-count">0</span> tarjetas</span>
    </div>
  </div>
</div>
<div class="nw-num" id="s07-n1" style="left:40px;top:548px">1</div>
<div class="nw-num" id="s07-n2" style="left:40px;top:708px">2</div>
<div class="nw-cursor" id="s07-cursor" style="left:1180px;top:860px">{CURSOR_SVG}</div>
<span class="nw-chip nw-abs" id="s07-label" style="left:120px;top:690px;background:#FBF5EC;color:#141A33">Paco · dueño de Pepito</span>
<div class="nw-abs" id="s07-fly" style="left:330px;top:745px"></div>
""",
    css="""
#s07 .s07-bubble { position: absolute; left: 0; top: 0; white-space: nowrap; background: #fff; border: 3px solid #E3E6EB; border-radius: 999px; padding: 10px 22px; font-weight: 800; font-size: 22px; box-shadow: 0 10px 24px rgba(20,26,51,.14); }
""",
    js=S07_PH[1] + """
  tl.fromTo(S("#s07-scrim"), { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power2.out" }, 2.0);
  tl.fromTo(S("#s07-intro"), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "power4.out" }, 0.5);
  tl.to(S("#s07-intro, #s07-label"), { y: -30, opacity: 0, duration: 0.25, ease: "power2.in" }, 2.0);
  tl.fromTo(S("#s07-panel"), { x: 140, opacity: 0, scale: 0.96 }, { x: 0, opacity: 1, scale: 1, duration: 0.5, ease: "expo.out" }, 2.2);
  tl.fromTo(S("#s07-cursor"), { opacity: 0 }, { opacity: 1, duration: 0.2, ease: "power1.out" }, 2.6);
  typeText("#s07-text", "2x1 en cañas este viernes", 2.9, 1.7);
  tl.fromTo(S("#s07-caret"), { opacity: 1 }, { opacity: 0, duration: 0.25, yoyo: true, repeat: 15, ease: "steps(1)" }, 0.5);
  // Cursor: click 1 on "Todos los clientes", click 2 on "Enviar".
  tl.fromTo(S("#s07-cursor"), { x: 0, y: 0 }, { x: -620, y: -360, duration: 0.7, ease: "power3.inOut" }, 4.8);
  tl.fromTo(S("#s07-all"), { borderColor: "#E3E6EB", color: "#141A33" }, { borderColor: "#1F5EFF", color: "#1F5EFF", duration: 0.15 }, 5.55);
  tl.fromTo(S("#s07-n1"), { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }, 5.55);
  tl.to(S("#s07-cursor"), { x: -760, y: -180, duration: 0.55, ease: "power3.inOut" }, 5.85);
  tl.fromTo(S("#s07-send"), { scale: 1 }, { scale: 0.92, duration: 0.1, yoyo: true, repeat: 1, ease: "power2.out" }, 6.45);
  tl.fromTo(S("#s07-n2"), { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }, 6.45);
  tl.fromTo(S("#s07-sent"), { x: -30, opacity: 0 }, { x: 0, opacity: 1, duration: 0.35, ease: "power3.out" }, 6.9);
  countUp("#s07-count", 318, 6.95, 1.3);
  tl.to(S("#s07-n1, #s07-n2"), { scale: 0, opacity: 0, duration: 0.25, ease: "power2.in" }, 8.0);
  // The promo flies out to customers' phones.
  const fly = document.querySelector(S("#s07-fly"));
  for (let i = 0; i < 7; i++) {
    const b = document.createElement("div");
    b.className = "s07-bubble";
    b.textContent = "2x1 en cañas este viernes";
    fly.appendChild(b);
    const a = (i / 6) * 1.2 - 0.6;
    tl.fromTo(b, { x: 0, y: 0, scale: 0.4, opacity: 0 },
      { x: -260 - 120 * Math.cos(a) * 3, y: -420 * Math.sin(a) - 120, scale: 1, opacity: 1, duration: 0.9, ease: "power2.out" }, 8.3 + i * 0.12);
    tl.to(b, { x: -1100, opacity: 0, duration: 0.8, ease: "power2.in" }, 9.6 + i * 0.12);
  }
""")

# ---------------------------------------------------------------- 08 notification (held)
S08_PH = photo("s08", [("s08-bolsillo", 0, (1.15, -140, 0), (1.22, -150, -20))])
SCENES[8] = dict(
    body=S08_PH[0] + f"""
<div class="nw-scrim" style="background:linear-gradient(to right, rgba(14,18,34,0) 35%, rgba(14,18,34,.7) 70%), linear-gradient(to top, rgba(14,18,34,.8) 0%, rgba(14,18,34,0) 40%)"></div>
<p class="nw-h nw-abs nw-ink" id="s08-h1" style="left:110px;top:800px;font-size:84px;white-space:nowrap">Y en el bolsillo de Lucía…</p>
<p class="nw-h nw-abs nw-ink" id="s08-h2" style="left:110px;top:900px;font-size:84px;white-space:nowrap"><span class="nw-blue">ahí está.</span></p>
<div class="nw-phone" id="s08-phone" style="left:1400px;top:120px">
  <div class="nw-notch"></div>
  <div class="nw-screen" style="background:#22305F">
    <div class="nw-h" style="color:#fff;text-align:center;font-size:110px;margin-top:120px">19:42</div>
    <div style="color:#fff;text-align:center;font-size:24px;font-weight:600;opacity:.85">jueves, 23 de octubre</div>
  </div>
</div>
<div class="nw-notif" id="s08-notif" style="left:1180px;top:420px;width:690px">
  <div class="nw-logo" style="width:84px;height:84px;font-size:44px">P</div>
  <div style="flex:1"><div class="t1">Restaurante Pepito · ahora</div><div class="t2">2x1 en cañas este viernes</div></div>
  {BEER_SVG.format(s=70)}
</div>
""",
    css="",
    js=S08_PH[1] + """
  tl.fromTo(S("#s08-phone"), { y: 120, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, 0);
  tl.fromTo(S("#s08-h1"), { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "power4.out" }, 0.3);
  tl.fromTo(S("#s08-notif"), { y: -260, opacity: 0, scale: 0.9 }, { y: 0, opacity: 1, scale: 1, duration: 0.55, ease: "back.out(1.5)" }, 1.6);
  tl.fromTo(S("#s08-h2"), { scale: 1.3, opacity: 0, transformOrigin: "0% 50%" }, { scale: 1, opacity: 1, duration: 0.4, ease: "power4.out" }, 1.75);
  // Held frame: nothing moves from 2.15 to 3.6.
  tl.fromTo(S("#s08-phone"), { scale: 1 }, { scale: 1.06, duration: D - 3.6, ease: "sine.inOut" }, 3.6);
  tl.fromTo(S("#s08-notif"), { scale: 1 }, { scale: 1.08, duration: D - 3.6, ease: "sine.inOut" }, 3.6);
""")

# ---------------------------------------------------------------- 09 she comes back
S09_PASS = pass_card("s09-pass", 1, 600)
S09_PH = photo("s09", [("s09-vuelve", 0, (1.05, 0, 0), (1.14, 20, 0)),
                       ("s09-brindis", 2.7, (1.14, 0, 0), (1.04, 0, 0))],
               box="left:80px;top:150px;width:1000px;height:800px", radius=30)
SCENES[9] = dict(
    body=f"""
""" + S09_PH[0] + f"""
<p class="nw-h nw-abs" id="s09-h" style="left:1140px;top:360px;font-size:96px;line-height:1">El viernes vuelve.<br><span class="nw-blue">Y no viene sola.</span></p>
<div class="nw-chip nw-abs" id="s09-day" style="left:110px;top:70px;background:#141A33;color:#FBF5EC">VIERNES · 20:30</div>
<div class="nw-abs" id="s09-passwrap" style="left:1140px;top:170px">{S09_PASS}</div>
<p class="nw-h nw-abs" id="s09-t1" style="left:1140px;top:730px;font-size:88px;white-space:nowrap">¡Sello <span class="nw-blue">sumado!</span></p>
<p class="nw-abs" id="s09-t2" style="left:1146px;top:850px;font-size:40px;font-weight:700;color:#5B6178">Llevas 2 de 5</p>
""",
    css="""
#s09-passwrap .nw-pass { position: relative; }
#s09-photo { box-shadow: 0 30px 60px rgba(20,26,51,.22); }
""",
    js=S09_PH[1] + """
  tl.fromTo(S("#s09-day"), { y: -30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }, IN);
  tl.fromTo(S("#s09-photo"), { x: -120, opacity: 0 }, { x: 0, opacity: 1, duration: 0.5, ease: "expo.out" }, 0.15);
  tl.fromTo(S("#s09-h"), { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "power4.out" }, 0.6);
  tl.to(S("#s09-h"), { y: -40, opacity: 0, duration: 0.25, ease: "power2.in" }, 2.7);
  tl.fromTo(S("#s09-passwrap"), { x: 120, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: "expo.out" }, 3.0);
  tl.fromTo(S("#s09-pass .nw-stamps i:nth-child(2) b"), { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2.2)" }, 3.4);
  tl.fromTo(S("#s09-t1"), { scale: 1.3, opacity: 0, transformOrigin: "0% 50%" }, { scale: 1, opacity: 1, duration: 0.4, ease: "power4.out" }, 3.55);
  tl.fromTo(S("#s09-t2"), { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }, 3.95);
  breath("#s09-passwrap", 4.4, 2.4, { y: -10 });
""")

# ---------------------------------------------------------------- 10 hinge
SCENES[10] = dict(
    body="""
<div class="nw-abs" style="inset:0;background:#1F5EFF"></div>
<div class="nw-ghost" id="s10-ghost" style="font-size:620px;left:-40px;top:160px;color:#fff;opacity:.12">MÁS</div>
<p class="nw-h nw-abs" id="s10-a" style="left:150px;top:330px;font-size:170px;color:#fff">Y esto es solo</p>
<p class="nw-h nw-abs" id="s10-b" style="left:150px;top:520px;font-size:170px;color:#fff">el principio.</p>
""",
    css="",
    js="""
  tl.fromTo(S("#s10-a"), { x: 300, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: "expo.out" }, 0.1);
  tl.fromTo(S("#s10-b"), { x: 300, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: "expo.out" }, 0.55);
  tl.fromTo(S("#s10-ghost"), { x: 0 }, { x: -300, duration: D, ease: "none" }, 0);
""")

# ---------------------------------------------------------------- 11 loyalty
S11_PH = photo("s11", [("s11-camarero", 0, (1.04, 0, 0), (1.16, -10, 10))],
               box="left:1240px;top:110px;width:600px;height:860px", radius=30)
SCENES[11] = dict(
    body=S11_PH[0] + f"""
<p class="nw-h nw-abs" id="s11-title" style="left:120px;top:120px;font-size:100px;white-space:nowrap">Tarjeta de <span class="nw-blue">fidelidad</span></p>
<div class="nw-abs" id="s11-passwrap" style="left:120px;top:330px">{pass_card("s11-pass", 0, 700, reward='<span id="s11-reward">Café gratis</span>')}</div>
<div class="nw-abs" id="s11-qr" style="left:880px;top:430px;width:200px;height:200px;border-radius:16px;border:14px solid #fff;box-shadow:0 20px 40px rgba(20,26,51,.2);background:conic-gradient(from 90deg at 50% 50%, #fff 25%, #0E1222 0 50%, #fff 0 75%, #0E1222 0) 0 0 / 43px 43px"></div>
<div class="nw-abs" id="s11-scan" style="left:880px;top:430px;width:200px;height:6px;background:#1B7F3B;box-shadow:0 0 18px #1B7F3B"></div>
<div class="nw-phone" id="s11-staff" style="left:1360px;top:150px">
  <div class="nw-notch"></div>
  <div class="nw-screen" style="background:#fff;display:flex;flex-direction:column;align-items:center;padding:110px 30px 0;gap:26px;text-align:center">
    <div style="font-weight:800;font-size:24px;color:#5B6178;letter-spacing:.1em">PERSONAL · PIN ✓</div>
    <div class="nw-logo" style="width:110px;height:110px;font-size:56px">P</div>
    <div style="font-weight:800;font-size:34px">5 / 5 sellos</div>
    <span class="nw-btn" id="s11-redeem" style="background:#1B7F3B;font-size:26px">Canjear premio</span>
    <div id="s11-ok" style="font-weight:800;font-size:30px;color:#1B7F3B">✓ Premio canjeado</div>
  </div>
</div>
""",
    css="#s11-passwrap .nw-pass { position: relative; } #s11-reward { display: inline-block; } #s11-photo { box-shadow: 0 30px 60px rgba(20,26,51,.22); }",
    js=S11_PH[1] + """
  tl.fromTo(S("#s11-photo"), { x: 120, opacity: 0 }, { x: 0, opacity: 1, duration: 0.5, ease: "expo.out" }, 0.3);
  tl.fromTo(S("#s11-title"), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.42, ease: "power4.out" }, IN);
  tl.fromTo(S("#s11-passwrap"), { x: -80, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: "expo.out" }, 0.75);
  gsap.utils.toArray(S("#s11-pass .nw-stamps i b")).forEach((b, i) => {
    tl.fromTo(b, { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.2)" }, 1.95 + i * 0.3);
  });
  tl.fromTo(S("#s11-reward"), { scale: 1, color: "#FFFFFF" }, { scale: 1.25, color: "#F4A12B", duration: 0.3, ease: "power3.out", transformOrigin: "0% 50%" }, 3.6);
  tl.to(S("#s11-reward"), { scale: 1, duration: 0.3, ease: "power3.out" }, 3.95);
  tl.fromTo(S("#s11-qr"), { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "power3.out" }, 4.55);
  tl.fromTo(S("#s11-staff"), { x: 500, rotation: 10 }, { x: 0, rotation: 0, duration: 0.6, ease: "expo.out" }, 4.75);
  tl.fromTo(S("#s11-scan"), { y: 0, opacity: 0 }, { y: 194, opacity: 1, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: 1 }, 5.3);
  tl.fromTo(S("#s11-redeem"), { scale: 1 }, { scale: 0.92, duration: 0.1, yoyo: true, repeat: 1 }, 6.3);
  tl.fromTo(S("#s11-ok"), { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "back.out(2)" }, 6.5);
  tl.set(S("#s11-scan"), { opacity: 0 }, 6.25);
  breath("#s11-staff", 7, 2.4, { y: -10 });
""")

# ---------------------------------------------------------------- 12 brand in the Wallet
SCENES[12] = dict(
    body=f"""
<div class="nw-panel" id="s12-panel" style="left:110px;top:150px;width:620px;height:720px">
  <div class="bar"><i></i><i></i><i></i><span style="margin-left:16px">Marca de la tarjeta</span></div>
  <div style="padding:40px;display:flex;flex-direction:column;gap:38px;font-size:28px;font-weight:800">
    <div>Logo<div class="nw-field" style="margin-top:14px;font-size:26px">pepito-logo.png ✓</div></div>
    <div>Color
      <div style="display:flex;gap:22px;margin-top:16px">
        <i class="s12-sw" style="background:#1F2937"></i><i class="s12-sw" id="s12-red" style="background:#8B1E3F"></i><i class="s12-sw" style="background:#0B6E4F"></i><i class="s12-sw" style="background:#E9852F"></i>
      </div>
    </div>
    <div>Carta<div class="nw-field" style="margin-top:14px;font-size:26px">pepito.es/carta</div></div>
  </div>
</div>
<div class="nw-cursor" id="s12-cursor" style="left:640px;top:900px">{CURSOR_SVG}</div>
<div class="nw-abs" id="s12-a" style="left:840px;top:130px">{pass_card("s12-pa", 2, 500, top_label="APPLE WALLET", extra='<div class="lbl s12-menu">Ver carta ›</div>')}</div>
<div class="nw-abs" id="s12-g" style="left:1370px;top:250px">{pass_card("s12-pg", 2, 500, top_label="GOOGLE WALLET", extra='<div class="lbl s12-menu">Ver carta ›</div>')}</div>
<p class="nw-h nw-abs" id="s12-t" style="left:800px;top:900px;font-size:76px;white-space:nowrap">Tu marca, <span class="nw-blue">en su bolsillo.</span></p>
""",
    css="""
#s12 .s12-sw { display: block; width: 74px; height: 74px; border-radius: 50%; }
#s12-red { box-shadow: 0 0 0 0 #1F5EFF; }
#s12 .nw-pass { position: relative; }
#s12 .s12-menu { opacity: 0; color: #fff; }
""",
    js="""
  tl.fromTo(S("#s12-panel"), { x: -100, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: "expo.out" }, 0.2);
  tl.fromTo(S("#s12-a"), { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "power3.out" }, 0.45);
  tl.fromTo(S("#s12-g"), { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "power3.out" }, 0.6);
  // "Tu logo": the logo pops on both cards.
  tl.fromTo(S(".nw-pass .nw-logo"), { scale: 0 }, { scale: 1, duration: 0.4, ease: "back.out(2)", stagger: 0.1 }, 0.85);
  // "tus colores": the cursor picks maroon and both cards repaint.
  tl.fromTo(S("#s12-cursor"), { x: 0, y: 0 }, { x: -390, y: -470, duration: 0.6, ease: "power3.inOut" }, 1.0);
  tl.fromTo(S("#s12-red"), { boxShadow: "0 0 0 0px #1F5EFF" }, { boxShadow: "0 0 0 8px #1F5EFF", duration: 0.2 }, 1.62);
  tl.fromTo(S(".nw-pass"), { backgroundColor: "#1F2937" }, { backgroundColor: "#8B1E3F", duration: 0.35, ease: "power2.out" }, 1.65);
  // "tu carta": the menu link appears on the back.
  tl.fromTo(S(".s12-menu"), { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out", stagger: 0.12 }, 2.4);
  // "Apple Wallet y Google Wallet": each card nods on its name.
  tl.fromTo(S("#s12-a"), { scale: 1 }, { scale: 1.05, duration: 0.2, yoyo: true, repeat: 1, ease: "power2.out" }, 3.15);
  tl.fromTo(S("#s12-g"), { scale: 1 }, { scale: 1.05, duration: 0.2, yoyo: true, repeat: 1, ease: "power2.out" }, 3.9);
  tl.fromTo(S("#s12-t"), { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.42, ease: "power4.out" }, 4.6);
  breath("#s12-g", 5.2, 2.6, { y: -12 });
""")

# ---------------------------------------------------------------- 13 two clicks
PHONES13 = "".join(f'<div class="s13-ph" style="left:{120 + i * 172}px"><div class="s13-n"></div></div>' for i in range(10))
SCENES[13] = dict(
    body=f"""
<p class="nw-h nw-abs" id="s13-q" style="left:120px;top:110px;font-size:110px">¿Una promoción?</p>
<div class="nw-abs" id="s13-steps" style="left:120px;top:280px;display:flex;align-items:center;gap:30px">
  <div class="nw-num" id="s13-n1" style="position:relative">1</div><div class="nw-h" id="s13-w1" style="font-size:110px">Escribe</div>
  <div class="nw-num" id="s13-n2" style="position:relative;margin-left:50px">2</div><div class="nw-h nw-blue" id="s13-w2" style="font-size:110px">Envía</div>
</div>
<div class="nw-abs" style="left:0;top:520px;width:1920px;height:440px">{PHONES13}</div>
<div class="nw-abs" id="s13-wave" style="left:0;top:500px;width:120px;height:480px;background:linear-gradient(90deg,rgba(31,94,255,0),rgba(31,94,255,.35),rgba(31,94,255,0))"></div>
""",
    css="""
#s13 .s13-ph { position: absolute; top: 40px; width: 140px; height: 290px; border-radius: 26px; background: #0E1222; padding: 8px; }
#s13 .s13-ph::after { content: ""; position: absolute; inset: 8px; border-radius: 20px; background: #22305F; }
#s13 .s13-n { position: absolute; left: 14px; right: 14px; top: 60px; height: 64px; border-radius: 14px; background: #fff; z-index: 2; opacity: 0;
  background-image: radial-gradient(circle at 22px 32px, #F4A12B 12px, transparent 13px); }
""",
    js="""
  tl.fromTo(S("#s13-q"), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.42, ease: "power4.out" }, IN);
  tl.fromTo(S("#s13-n1"), { scale: 0 }, { scale: 1, duration: 0.3, ease: "back.out(2)" }, 1.55);
  tl.fromTo(S("#s13-w1"), { x: -60, opacity: 0 }, { x: 0, opacity: 1, duration: 0.35, ease: "expo.out" }, 1.6);
  tl.fromTo(S("#s13-n2"), { scale: 0 }, { scale: 1, duration: 0.3, ease: "back.out(2)" }, 2.05);
  tl.fromTo(S("#s13-w2"), { x: -60, opacity: 0 }, { x: 0, opacity: 1, duration: 0.35, ease: "expo.out" }, 2.1);
  tl.fromTo(S(".s13-ph"), { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out", stagger: 0.04 }, 2.4);
  tl.fromTo(S("#s13-wave"), { x: -150, opacity: 0 }, { x: 1950, opacity: 1, duration: 1.0, ease: "power1.inOut" }, 3.1);
  gsap.utils.toArray(S(".s13-n")).forEach((n, i) => {
    tl.fromTo(n, { y: -30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: "back.out(1.8)" }, 3.15 + i * 0.09);
  });
  breath(".s13-ph", 4.6, 2.2, { y: -8 });
""")

# ---------------------------------------------------------------- 14 and more
TILES = [("pin", "Avisos al pasar cerca"), ("chart", "Estadísticas por mesa"), ("store", "Todos tus locales en una cuenta"),
         ("lock", "Tags NFC imposibles de copiar"), ("receipt", "Facturas automáticas"), ("shield", "RGPD de serie")]
TILE_HTML = ""
for i, (ic, label) in enumerate(TILES):
    col, row = i % 3, i // 3
    focus = i == 2
    style = (f"left:{120 + col * 570}px;top:{260 + row * 360}px;"
             + ("background:#1F5EFF;color:#fff;border-color:#1F5EFF" if focus else ""))
    TILE_HTML += (f'<div class="s14-tile" id="s14-t{i + 1}" style="{style}">'
                  f'{ICON(ic, "#fff" if focus else "#1F5EFF", 96)}<div>{label}</div></div>')
SCENES[14] = dict(
    body=f"""
<p class="nw-h nw-abs" id="s14-title" style="left:120px;top:90px;font-size:110px">Y además…</p>
{TILE_HTML}
""",
    css="""
#s14 .s14-tile { position: absolute; width: 540px; height: 320px; background: #fff; border: 5px solid #141A33; border-radius: 34px;
  padding: 40px 44px; display: flex; flex-direction: column; justify-content: space-between; font-weight: 800; font-size: 42px; line-height: 1.12; }
#s14 .bar1, #s14 .bar2, #s14 .bar3 { transform-box: fill-box; transform-origin: 50% 100%; }
""",
    js="""
  tl.fromTo(S("#s14-title"), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.42, ease: "power4.out" }, IN);
  [0.6, 2.1, 3.5, 5.6, 7.9, 8.25].forEach((t, i) => {
    tl.fromTo(S("#s14-t" + (i + 1)), { y: 70, scale: 0.9, opacity: 0 }, { y: 0, scale: 1, opacity: 1, duration: 0.42, ease: "power3.out" }, t);
  });
  tl.fromTo(S("#s14-t2 .bar1, #s14-t2 .bar2, #s14-t2 .bar3"), { scaleY: 0 }, { scaleY: 1, duration: 0.5, ease: "power3.out", stagger: 0.1 }, 2.35);
  tl.fromTo(S("#s14-t1 svg"), { y: 0 }, { y: -10, duration: 0.35, yoyo: true, repeat: 3, ease: "sine.inOut" }, 1.0);
  tl.fromTo(S("#s14-t4 svg"), { rotation: 0 }, { rotation: -8, duration: 0.12, yoyo: true, repeat: 3, ease: "sine.inOut" }, 7.3);
  breath("#s14-t3", 4.0, 2.4, { scale: 1.03 });
""")

# ---------------------------------------------------------------- 15 close
S15_PH = photo("s15", [("s15-local", 0, (1.06, 0, 0), (1.16, 0, -20))])
SCENES[15] = dict(
    body=S15_PH[0] + f"""
<div class="nw-scrim" id="s15-scrim" style="background:rgba(14,18,34,.66)"></div>
<div class="nw-abs" style="left:0;right:0;top:250px;display:flex;align-items:center;justify-content:center;gap:40px">
  <div id="s15-icon" style="width:190px;height:190px;border-radius:46px;background:#1F5EFF;display:grid;place-items:center">{NFC_WAVES("#fff", 120, 6)}</div>
  <div class="nw-h nw-ink" id="s15-word" style="font-size:180px">NFC Wallet</div>
</div>
<p class="nw-h nw-abs nw-ink" id="s15-claim" style="left:0;right:0;top:530px;text-align:center;font-size:92px">Tus clientes vuelven <span class="nw-blue">solos.</span></p>
<p class="nw-abs nw-ink" id="s15-price" style="left:0;right:0;top:680px;text-align:center;font-size:44px;font-weight:700">Desde 29 €/mes por restaurante · 14 días gratis</p>
<div class="nw-abs" id="s15-url" style="left:0;right:0;top:790px;display:flex;justify-content:center"><span class="nw-btn" id="s15-btn" style="background:#1F5EFF;font-size:52px;padding:26px 70px">nfcwallet.es</span></div>
""",
    css="#s15-icon path { stroke-dasharray: 60; }",
    js=S15_PH[1] + """
  tl.fromTo(S("#s15-icon"), { scale: 0, rotation: -20 }, { scale: 1, rotation: 0, duration: 0.5, ease: "power3.out" }, IN);
  tl.fromTo(S("#s15-icon path"), { strokeDashoffset: 60 }, { strokeDashoffset: 0, duration: 0.5, ease: "power2.out", stagger: 0.12 }, 0.45);
  tl.fromTo(S("#s15-word"), { x: -80, opacity: 0, scale: 1.08, transformOrigin: "0% 50%" }, { x: 0, opacity: 1, scale: 1, duration: 0.6, ease: "expo.out" }, 0.5);
  tl.fromTo(S("#s15-claim"), { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "power4.out" }, 1.2);
  tl.fromTo(S("#s15-price"), { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 3.0);
  tl.fromTo(S("#s15-url"), { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.8)" }, 4.3);
  tl.fromTo(S("#s15-btn"), { boxShadow: "0 0 0 0px rgba(31,94,255,.35)" }, { boxShadow: "0 0 0 26px rgba(31,94,255,0)", duration: 1.1, ease: "power2.out", repeat: 4 }, 5.0);
  tl.fromTo(S("#s15-scrim"), { opacity: 0.35 }, { opacity: 1, duration: 0.6, ease: "power2.out" }, 0);
""")


# ---------------------------------------------------------------- pace beats
# Extra beats that fill the holds flagged by the animation map (no dead zone > 1 s).
EXTRA = {
    2: dict(body="""
<div class="nw-abs" id="s02-mesa" style="left:1560px;top:80px"><span class="nw-chip" style="background:#FBF5EC;color:#141A33">Mesa 4</span></div>
""", css="", js="""
  tl.fromTo(S("#s02-mesa"), { y: -30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "back.out(2)" }, 5.4);
"""),
    3: dict(body="""<span class="nw-chip nw-abs" id="s03-c3" style="right:120px;top:780px;background:#141A33;color:#FBF5EC">Funciona en iPhone y Android</span>""",
            css="", js="""
  tl.fromTo(S("#s03-c3"), { x: 80, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 6.9);
  tl.fromTo(S("#s03-landing .nw-btn"), { scale: 1 }, { scale: 1.06, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut" }, 7.8);
"""),
    4: dict(body="""
<div class="nw-abs" id="s04-wl" style="left:1440px;top:170px;display:flex;flex-direction:column;gap:16px">
  <span class="nw-chip" id="s04-wa" style="background:#141A33;color:#FBF5EC">Apple Wallet</span>
  <span class="nw-chip" id="s04-wg" style="background:#fff;color:#141A33;border:3px solid #141A33">Google Wallet</span>
</div>
<div class="nw-abs" id="s04-shine" style="left:760px;top:150px;width:640px;height:600px;border-radius:30px;overflow:hidden;pointer-events:none">
  <div id="s04-gloss" style="position:absolute;top:-50%;left:0;width:140px;height:200%;background:rgba(255,255,255,.22);transform:rotate(18deg)"></div>
</div>
""", css="", js="""
  tl.fromTo(S("#s04-wa"), { x: 60, opacity: 0 }, { x: 0, opacity: 1, duration: 0.35, ease: "power3.out" }, 4.9);
  tl.fromTo(S("#s04-wg"), { x: 60, opacity: 0 }, { x: 0, opacity: 1, duration: 0.35, ease: "power3.out" }, 5.3);
  tl.fromTo(S("#s04-gloss"), { x: -260 }, { x: 900, duration: 0.8, ease: "power2.inOut" }, 6.2);
  tl.fromTo(S("#s04-passwrap"), { rotationY: 0 }, { rotationY: 8, duration: 0.6, yoyo: true, repeat: 1, ease: "sine.inOut", transformPerspective: 1200 }, 7.0);
"""),
    5: dict(body="", css="", js="""
  tl.fromTo(S("#s05-title"), { scale: 1 }, { scale: 1.06, duration: 0.25, yoyo: true, repeat: 1, ease: "power2.out", transformOrigin: "0% 50%" }, 7.6);
"""),
    7: dict(body="""<p class="nw-h nw-abs nw-ink" id="s07-done" style="left:110px;top:910px;font-size:96px;white-space:nowrap">Dos clics. <span class="nw-blue">Listo.</span></p>""",
            css="", js="""
  tl.fromTo(S("#s07-label"), { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 0.9);
  tl.fromTo(S("#s07-done"), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.42, ease: "power4.out" }, 11.2);
"""),
    9: dict(body="""
<p class="nw-abs" id="s09-t3" style="left:1146px;top:920px;font-size:40px;font-weight:800;color:#1F5EFF">Ha vuelto gracias a tu promo.</p>
""", css="", js="""
  tl.fromTo(S("#s09-t3"), { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 6.1);
"""),
    11: dict(body="""<span class="nw-chip nw-abs" id="s11-cfg" style="left:120px;top:830px;background:#141A33;color:#FBF5EC">Tú eliges el premio y los sellos</span>""",
             css="", js="""
  tl.fromTo(S("#s11-cfg"), { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 8.1);
  tl.fromTo(S("#s11-passwrap"), { rotation: 0 }, { rotation: -2, duration: 0.5, yoyo: true, repeat: 1, ease: "sine.inOut" }, 8.6);
"""),
    12: dict(body="", css="", js="""
  tl.to(S("#s12-cursor"), { x: -250, y: -470, duration: 0.45, ease: "power3.inOut" }, 6.5);
  tl.to(S("#s12-red"), { boxShadow: "0 0 0 0px #1F5EFF", duration: 0.15 }, 7.0);
  tl.fromTo(S(".s12-sw:nth-child(3)"), { boxShadow: "0 0 0 0px #1F5EFF" }, { boxShadow: "0 0 0 8px #1F5EFF", duration: 0.2 }, 7.0);
  tl.to(S(".nw-pass"), { backgroundColor: "#0B6E4F", duration: 0.35, ease: "power2.out" }, 7.05);
  tl.to(S("#s12-cursor"), { x: -390, y: -470, duration: 0.45, ease: "power3.inOut" }, 7.9);
  tl.to(S(".s12-sw:nth-child(3)"), { boxShadow: "0 0 0 0px #1F5EFF", duration: 0.15 }, 8.4);
  tl.to(S("#s12-red"), { boxShadow: "0 0 0 8px #1F5EFF", duration: 0.2 }, 8.4);
  tl.to(S(".nw-pass"), { backgroundColor: "#8B1E3F", duration: 0.35, ease: "power2.out" }, 8.45);
"""),
    13: dict(body="""<p class="nw-h nw-abs" id="s13-now" style="left:120px;top:900px;font-size:96px;white-space:nowrap">Al instante. <span class="nw-blue">A todos.</span></p>""",
             css="", js="""
  tl.fromTo(S(".s13-ph"), { rotation: 0 }, { rotation: 3, duration: 0.05, yoyo: true, repeat: 7, ease: "none", stagger: 0.03 }, 6.0);
  tl.fromTo(S("#s13-now"), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.42, ease: "power4.out" }, 4.4);
  tl.fromTo(S("#s13-wave"), { x: -150, opacity: 0 }, { x: 1950, opacity: 1, duration: 1.0, ease: "power1.inOut", immediateRender: false }, 7.2);
"""),
    14: dict(body="""<p class="nw-h nw-abs" id="s14-all" style="left:930px;top:135px;font-size:50px;white-space:nowrap;color:#1F5EFF">Todo en un mismo panel.</p>""",
             css="", js="""
  tl.fromTo(S("#s14-t2 .bar1, #s14-t2 .bar2, #s14-t2 .bar3"), { scaleY: 1 }, { scaleY: 0.4, duration: 0.3, yoyo: true, repeat: 1, ease: "sine.inOut", stagger: 0.1, immediateRender: false }, 6.5);
  tl.fromTo(S("#s14-all"), { x: 80, opacity: 0 }, { x: 0, opacity: 1, duration: 0.42, ease: "expo.out" }, 9.0);
"""),
    15: dict(body="", css="", js="""
  tl.fromTo(S("#s15-icon path"), { opacity: 1 }, { opacity: 0.25, duration: 0.25, yoyo: true, repeat: 1, ease: "sine.inOut", stagger: 0.12 }, 6.6);
  tl.fromTo(S("#s15-icon path"), { opacity: 1 }, { opacity: 0.25, duration: 0.25, yoyo: true, repeat: 1, ease: "sine.inOut", stagger: 0.12, immediateRender: false }, 8.4);
  tl.fromTo(S("#s15-word"), { y: 0 }, { y: -8, duration: 1.2, yoyo: true, repeat: 1, ease: "sine.inOut" }, 7.0);
  // Final scene only: everything fades to the cream canvas.
  tl.to(S("#s15-fade"), { opacity: 1, duration: 0.8, ease: "power1.in" }, D - 0.85);
"""),
}
EXTRA[15]["body"] = '<div class="nw-abs" id="s15-fade" style="inset:0;background:#FBF5EC;opacity:0;z-index:10"></div>'
for n, ex in EXTRA.items():
    SCENES[n]["body"] += ex["body"]
    SCENES[n]["css"] += "\n" + ex["css"]
    SCENES[n]["js"] += ex["js"]


# ---------------------------------------------------------------- audio plan
# v3: no voice-over and no SFX; the only audio is the Lyria music bed.
MUSIC = "assets/music/lyria.wav"
FADE_IN, FADE_OUT = 0.4, 2.0


def build():
    comp = ROOT / "compositions"
    comp.mkdir(exist_ok=True)
    for n, sc in SCENES.items():
        sid = f"s{n:02d}"
        (comp / f"{sid}.html").write_text(scene(sid, n, sc["body"], sc["css"], sc["js"]))

    slots, trans, audio = [], [], []
    for n in range(1, 16):
        start, dur, ov = slot(n)
        sid = f"s{n:02d}"
        slots.append(f'      <div id="el-{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                     f'data-start="{start}" data-duration="{dur}" data-track-index="{1 + (n + 1) % 2}" '
                     f'data-width="{W}" data-height="{H}" style="z-index:{n}"></div>')
        kind = TIN[n][0]
        if kind in ("push", "whip") and n > 1:
            prev = f"el-s{n - 1:02d}"
            blur = "blur(12px)" if kind == "whip" else "blur(0px)"
            ease = "power4.inOut" if kind == "push" else "expo.inOut"
            trans.append(f'      tl.fromTo("#{prev}", {{ xPercent: 0, filter: "blur(0px)" }}, {{ xPercent: -100, filter: "{blur}", duration: {ov}, ease: "{ease}", immediateRender: false }}, {start});')
            trans.append(f'      tl.fromTo("#el-{sid}", {{ xPercent: 100, filter: "{blur}" }}, {{ xPercent: 0, filter: "blur(0px)", duration: {ov}, ease: "{ease}" }}, {start});')

    # Music bed with a fade-in/out volume lane; nothing to duck under.
    auto = {"version": 1, "lanes": [{"target": "volume", "points": [
        {"t": 0, "v": 0}, {"t": FADE_IN, "v": 1}, {"t": TOTAL - FADE_OUT, "v": 1}, {"t": TOTAL, "v": 0}]}]}
    value = html.escape(json.dumps(auto, separators=(",", ":")), quote=True)
    audio.append(f'      <audio id="bgm" src="{MUSIC}" data-start="0" data-duration="{TOTAL}" '
                 f'data-track-index="10" data-volume="0.8" data-automation="{value}"></audio>')

    index = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>NFC Wallet · vídeo promocional</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #FBF5EC; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #FBF5EC; }}
      #root > div[data-composition-src] {{ position: absolute; inset: 0; will-change: transform; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
{chr(10).join(slots)}
{chr(10).join(audio)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // Leftward push / whip transitions between scene slots (all <= 0.35 s).
{chr(10).join(trans)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    (ROOT / "index.html").write_text(index)
    print("built", len(SCENES), "scenes;", len(audio), "audio clips; total", TOTAL, "s")


if __name__ == "__main__":
    build()
