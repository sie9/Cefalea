#!/usr/bin/env python3
"""Generates the NFC Wallet promo compositions (16:9 master).

Writes compositions/sNN.html (one sub-composition per storyboard frame) and
index.html (slots, leftward push/whip transitions, voice-over, SFX and the
ducked music bed). Run from the project root: python3 tools/build.py
"""
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
W, H = 1920, 1080

# Scene boundaries snapped to strong beats of assets/music/bed-v2.wav (see beats/).
B = [0, 6, 14, 23.812, 33, 42, 48, 62, 70.066, 80.062, 83.847, 94.4, 103.967, 113, 123.681, 135]
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

SHARED_CSS = FONTS + """
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


def lucia(cls="", jacket="#F4A12B"):
    """Flat Lucía figure, 220x560 viewBox, feet at y=560."""
    return f"""<svg class="{cls}" viewBox="0 0 220 560" width="220" height="560">
  <g class="legs"><rect x="72" y="380" width="30" height="170" rx="14" fill="#141A33"/><rect x="118" y="380" width="30" height="170" rx="14" fill="#141A33"/>
  <ellipse cx="86" cy="552" rx="26" ry="10" fill="#0E1222"/><ellipse cx="134" cy="552" rx="26" ry="10" fill="#0E1222"/></g>
  <rect class="arm-l" x="38" y="200" width="30" height="170" rx="15" fill="{jacket}"/>
  <rect class="arm-r" x="152" y="200" width="30" height="170" rx="15" fill="{jacket}"/>
  <rect x="58" y="180" width="104" height="220" rx="46" fill="{jacket}"/>
  <rect x="98" y="182" width="24" height="60" rx="8" fill="#E8B48F"/>
  <circle cx="110" cy="120" r="58" fill="#E8B48F"/>
  <path d="M52 118 q0-72 58-72 q62 0 58 66 q-18-34-58-34 q-36 0-58 40z" fill="#2B2A3A"/>
  <circle cx="92" cy="128" r="6" fill="#2B2A3A"/><circle cx="128" cy="128" r="6" fill="#2B2A3A"/>
  <path d="M96 150 q14 12 28 0" stroke="#2B2A3A" stroke-width="5" fill="none" stroke-linecap="round"/>
</svg>"""


def friend(cls, skin, top, hair):
    return f"""<svg class="{cls}" viewBox="0 0 220 560" width="200" height="510">
  <rect x="72" y="380" width="30" height="170" rx="14" fill="#141A33"/><rect x="118" y="380" width="30" height="170" rx="14" fill="#141A33"/>
  <rect x="40" y="200" width="30" height="160" rx="15" fill="{top}"/><rect x="150" y="200" width="30" height="160" rx="15" fill="{top}"/>
  <rect x="58" y="180" width="104" height="220" rx="46" fill="{top}"/>
  <circle cx="110" cy="120" r="56" fill="{skin}"/>
  <path d="M54 112 q4-64 56-64 q54 0 56 64 q-20-28-56-28 q-38 0-56 28z" fill="{hair}"/>
  <circle cx="92" cy="128" r="6" fill="#2B2A3A"/><circle cx="128" cy="128" r="6" fill="#2B2A3A"/>
  <path d="M96 150 q14 12 28 0" stroke="#2B2A3A" stroke-width="5" fill="none" stroke-linecap="round"/>
</svg>"""


def paco(cls=""):
    """Flat Paco (owner) figure, bust, 360x520 viewBox."""
    return f"""<svg class="{cls}" viewBox="0 0 360 520" width="360" height="520">
  <rect x="70" y="250" width="220" height="270" rx="90" fill="#141A33"/>
  <rect x="110" y="270" width="140" height="250" rx="22" fill="#1F5EFF"/>
  <rect class="paco-arm" x="250" y="280" width="54" height="190" rx="27" fill="#141A33" style="transform-origin:277px 300px"/>
  <rect x="50" y="280" width="54" height="190" rx="27" fill="#141A33"/>
  <circle cx="180" cy="150" r="92" fill="#C98B62"/>
  <path d="M100 170 q80 120 160 0 v20 q-80 100 -160 0z" fill="#3B2A20"/>
  <circle cx="148" cy="138" r="9" fill="#2B2A3A"/><circle cx="212" cy="138" r="9" fill="#2B2A3A"/>
  <path d="M130 108 h34 M196 108 h34" stroke="#3B2A20" stroke-width="9" stroke-linecap="round"/>
  <path d="M158 196 q22 16 44 0" stroke="#FBF5EC" stroke-width="7" fill="none" stroke-linecap="round"/>
</svg>"""


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
SCENES[2] = dict(
    body=f"""
<div id="s02-world" class="nw-abs" data-layout-allow-overflow style="left:0;top:0;width:2700px;height:1080px">
  <svg class="nw-abs" style="left:0;top:0" width="2700" height="1080" viewBox="0 0 2700 1080">
    <rect width="2700" height="1080" fill="#FBF5EC"/>
    <rect x="0" y="930" width="2700" height="150" fill="#EFE2CC"/>
    <rect x="120" y="210" width="1080" height="720" rx="18" fill="#F1E3CC"/>
    <rect x="120" y="150" width="1080" height="110" rx="18" fill="#141A33"/>
    <text x="660" y="225" font-family="Archivo Black" font-size="64" fill="#F4A12B" text-anchor="middle">RESTAURANTE PEPITO</text>
    <rect x="250" y="360" width="290" height="570" rx="14" fill="#B9773E"/>
    <rect x="276" y="390" width="238" height="300" rx="10" fill="#F4A12B" opacity=".5"/>
    <circle cx="500" cy="660" r="12" fill="#F4A12B"/>
    <rect x="680" y="360" width="400" height="300" rx="14" fill="#FFE2B0"/>
    <rect x="680" y="360" width="400" height="56" fill="#E9852F"/>
    <path d="M680 416 h400" stroke="#C9661F" stroke-width="6"/>
    <circle cx="760" cy="520" r="26" fill="#F4A12B"/><circle cx="880" cy="500" r="26" fill="#F4A12B"/><circle cx="1000" cy="520" r="26" fill="#F4A12B"/>
    <rect x="1400" y="250" width="1200" height="680" rx="18" fill="#F6EBDA"/>
    <g fill="#F4A12B"><circle cx="1600" cy="300" r="20"/><circle cx="1900" cy="300" r="20"/><circle cx="2200" cy="300" r="20"/><circle cx="2500" cy="300" r="20"/></g>
    <g stroke="#E3D3BA" stroke-width="4"><path d="M1600 250 v30 M1900 250 v30 M2200 250 v30 M2500 250 v30"/></g>
    <rect x="1950" y="700" width="560" height="26" rx="10" fill="#B9773E"/>
    <rect x="2210" y="726" width="40" height="204" fill="#8E5A2C"/>
    <rect x="2120" y="900" width="220" height="30" rx="10" fill="#8E5A2C"/>
    <rect x="1800" y="640" width="150" height="20" rx="8" fill="#141A33"/><rect x="1800" y="640" width="20" height="290" rx="8" fill="#141A33"/>
    <rect x="1930" y="640" width="20" height="290" rx="8" fill="#141A33"/>
    <rect x="2330" y="672" width="40" height="28" rx="6" fill="#FBF5EC"/>
    <text x="2350" y="694" font-family="Archivo Black" font-size="16" fill="#1F5EFF" text-anchor="middle">NFC</text>
  </svg>
  <div class="nw-abs" id="s02-lucia" style="left:420px;top:380px">{lucia("s02-fig")}</div>
  <div class="nw-abs" id="s02-phone" style="left:2280px;top:672px;width:84px;height:28px;border-radius:8px;background:#0E1222"></div>
</div>
<div class="nw-meta" style="left:120px;top:70px" id="s02-tag">Restaurante Pepito · 14:05</div>
""",
    css="#s02-lucia svg { display: block; }",
    js="""
  // Camera pan door → table (the world moves left).
  tl.fromTo(S("#s02-world"), { x: 0 }, { x: -780, duration: 5.6, ease: "power2.inOut" }, 0.2);
  tl.fromTo(S("#s02-tag"), { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, IN);
  // Lucía walks from the door to the chair (bob while walking).
  tl.fromTo(S("#s02-lucia"), { x: 0 }, { x: 1400, duration: 4.3, ease: "power1.inOut" }, 0.5);
  tl.fromTo(S("#s02-lucia"), { y: 0 }, { y: -14, duration: 0.27, ease: "sine.inOut", yoyo: true, repeat: 15 }, 0.5);
  // Sits down.
  tl.to(S("#s02-lucia"), { y: 70, scaleY: 0.9, transformOrigin: "50% 100%", duration: 0.45, ease: "power3.out" }, 4.85);
  // Phone lands on the table on "deja el móvil".
  tl.fromTo(S("#s02-phone"), { y: -150, opacity: 0, rotation: -18 },
    { y: 0, opacity: 1, rotation: 0, duration: 0.45, ease: "bounce.out" }, 4.55);
""")

# ---------------------------------------------------------------- 03 tap
SCENES[3] = dict(
    body=f"""
<svg class="nw-abs" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">
  <rect width="1920" height="1080" fill="#C98B4E"/>
  <g stroke="#B9773E" stroke-width="10"><path d="M0 250 H1920 M0 520 H1920 M0 790 H1920"/></g>
  <g stroke="#D69A5C" stroke-width="4" opacity=".6"><path d="M0 120 H1920 M0 380 H1920 M0 650 H1920 M0 930 H1920"/></g>
</svg>
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
    js="""
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
SCENES[5] = dict(
    body=f"""
<div class="nw-abs" id="s05-passwrap" style="left:120px;top:150px">{pass_card("s05-pass", 0, 600)}</div>
<p class="nw-h nw-abs nw-blue" id="s05-title" style="left:120px;top:730px;font-size:92px;white-space:nowrap">Primer sello.</p>
<div class="nw-abs s05-tile" id="s05-t1" style="left:860px;top:130px;background:#FFE2B0">
  <svg viewBox="0 0 200 200" width="200" height="200"><circle cx="100" cy="100" r="84" fill="#fff"/><circle cx="100" cy="100" r="56" fill="#E9852F"/><circle cx="84" cy="88" r="10" fill="#F4A12B"/><circle cx="114" cy="110" r="12" fill="#B9773E"/></svg>
</div>
<div class="nw-abs s05-tile" id="s05-t2" style="left:1190px;top:130px;background:#F1E3CC">
  <svg viewBox="0 0 200 200" width="200" height="200"><g id="s05-glass-l"><rect x="40" y="60" width="50" height="110" rx="8" fill="#F4A12B"/><rect x="40" y="48" width="50" height="22" rx="10" fill="#fff"/></g><g id="s05-glass-r"><rect x="110" y="60" width="50" height="110" rx="8" fill="#F4A12B"/><rect x="110" y="48" width="50" height="22" rx="10" fill="#fff"/></g></svg>
</div>
<div class="nw-abs s05-tile" id="s05-t3" style="left:1520px;top:130px;background:#E7ECFF">
  <svg viewBox="0 0 200 200" width="200" height="200"><rect x="50" y="30" width="100" height="140" rx="10" fill="#fff"/><path d="M68 64h64M68 90h64M68 116h40" stroke="#5B6178" stroke-width="9" stroke-linecap="round"/><text x="100" y="158" font-family="Archivo Black" font-size="26" text-anchor="middle" fill="#1F5EFF">PAGADO</text></svg>
</div>
<div class="nw-abs" id="s05-door" style="left:860px;top:450px;width:940px;height:500px;border-radius:30px;background:#F1E3CC;overflow:hidden">
  <svg class="nw-abs" style="left:0;top:0" width="940" height="500" viewBox="0 0 940 500"><rect x="560" y="60" width="220" height="440" rx="12" fill="#B9773E"/><rect x="580" y="84" width="180" height="200" rx="8" fill="#F4A12B" opacity=".5"/><text x="300" y="120" font-family="Archivo Black" font-size="46" fill="#141A33" text-anchor="middle">¡Hasta pronto!</text></svg>
  <div class="nw-abs" id="s05-lucia" style="left:330px;top:150px;transform-origin:50% 100%">{lucia("s05-fig")}</div>
</div>
""",
    css="""
#s05 .s05-tile { width: 280px; height: 280px; border-radius: 30px; display: grid; place-items: center; box-shadow: 0 20px 40px rgba(20,26,51,.12); }
#s05-passwrap .nw-pass { position: relative; }
#s05-lucia svg { width: 150px; height: 382px; display: block; }
""",
    js="""
  tl.fromTo(S("#s05-passwrap"), { x: -60, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 0.1);
  tl.fromTo(S("#s05-pass .nw-stamps i:first-child b"), { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2.2)" }, 0.6);
  tl.fromTo(S("#s05-title"), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.42, ease: "power4.out" }, 0.75);
  ["#s05-t1", "#s05-t2", "#s05-t3"].forEach((id, i) => {
    tl.fromTo(S(id), { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.35, ease: "power3.out" }, 1.55 + i * 0.42);
  });
  tl.fromTo(S("#s05-glass-l"), { rotation: 0, transformOrigin: "50% 100%" }, { rotation: 12, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out" }, 2.1);
  tl.fromTo(S("#s05-glass-r"), { rotation: 0, transformOrigin: "50% 100%" }, { rotation: -12, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out" }, 2.1);
  tl.fromTo(S("#s05-door"), { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "expo.out" }, 2.8);
  // Lucía waves and walks out through the door.
  tl.fromTo(S("#s05-lucia .arm-r"), { rotation: 0, transformOrigin: "167px 210px" }, { rotation: -150, duration: 0.3, ease: "power2.out" }, 3.2);
  tl.to(S("#s05-lucia .arm-r"), { rotation: -120, duration: 0.22, yoyo: true, repeat: 5, ease: "sine.inOut" }, 3.5);
  tl.to(S("#s05-lucia .arm-r"), { rotation: 0, duration: 0.25, ease: "power2.in" }, 4.9);
  tl.fromTo(S("#s05-lucia"), { x: 0 }, { x: 330, duration: 1.4, ease: "power1.in" }, 5.2);
  tl.fromTo(S("#s05-lucia"), { opacity: 1 }, { opacity: 0, duration: 0.3 }, 6.3);
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
SCENES[7] = dict(
    body=f"""
<div class="nw-ghost" style="font-size:420px;left:-40px;bottom:-90px">PROMO</div>
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
<div class="nw-abs" id="s07-paco" style="left:1370px;top:380px">{paco("s07-fig")}</div>
<div class="nw-abs" id="s07-label" style="left:1350px;top:150px;font-weight:800;font-size:30px;color:#5B6178">Paco · dueño de Pepito</div>
<div class="nw-abs" id="s07-fly" style="left:330px;top:745px"></div>
""",
    css="""
#s07-paco svg { width: 430px; height: 621px; display: block; }
#s07 .s07-bubble { position: absolute; left: 0; top: 0; white-space: nowrap; background: #fff; border: 3px solid #E3E6EB; border-radius: 999px; padding: 10px 22px; font-weight: 800; font-size: 22px; box-shadow: 0 10px 24px rgba(20,26,51,.14); }
""",
    js="""
  tl.fromTo(S("#s07-panel"), { x: 140, opacity: 0, scale: 0.96 }, { x: 0, opacity: 1, scale: 1, duration: 0.5, ease: "expo.out" }, 0.45);
  tl.fromTo(S("#s07-paco"), { y: 120, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, 0.6);
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
  tl.fromTo(S("#s07-paco .paco-arm"), { rotation: 0 }, { rotation: -150, duration: 0.4, ease: "back.out(1.6)" }, 7.6);
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
  breath("#s07-paco", 8.2, 2.4, { y: -10 });
""")

# ---------------------------------------------------------------- 08 notification (held)
SCENES[8] = dict(
    body=f"""
<div class="nw-abs" style="inset:0;background:#141A33"></div>
<div class="nw-abs" id="s08-glow" style="left:460px;top:-200px;width:1000px;height:1000px;border-radius:50%;background:radial-gradient(circle,rgba(31,94,255,.35),rgba(31,94,255,0) 66%)"></div>
<div class="nw-phone" id="s08-phone" style="left:770px;top:120px">
  <div class="nw-notch"></div>
  <div class="nw-screen" style="background:#22305F">
    <div class="nw-h" style="color:#fff;text-align:center;font-size:110px;margin-top:120px">19:42</div>
    <div style="color:#fff;text-align:center;font-size:24px;font-weight:600;opacity:.85">jueves, 23 de octubre</div>
  </div>
</div>
<div class="nw-notif" id="s08-notif" style="left:560px;top:420px;width:800px">
  <div class="nw-logo" style="width:84px;height:84px;font-size:44px">P</div>
  <div style="flex:1"><div class="t1">Restaurante Pepito · ahora</div><div class="t2">2x1 en cañas este viernes</div></div>
  {BEER_SVG.format(s=70)}
</div>
""",
    css="",
    js="""
  tl.fromTo(S("#s08-phone"), { y: 120, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, 0);
  tl.fromTo(S("#s08-notif"), { y: -260, opacity: 0, scale: 0.9 }, { y: 0, opacity: 1, scale: 1, duration: 0.55, ease: "back.out(1.5)" }, 1.6);
  // Held frame: nothing moves from 2.15 to 3.6.
  tl.fromTo(S("#s08-phone"), { scale: 1 }, { scale: 1.06, duration: D - 3.6, ease: "sine.inOut" }, 3.6);
  tl.fromTo(S("#s08-notif"), { scale: 1 }, { scale: 1.08, duration: D - 3.6, ease: "sine.inOut" }, 3.6);
  breath("#s08-glow", 3.6, 2.4, { scale: 1.12 });
""")

# ---------------------------------------------------------------- 09 she comes back
S09_PASS = pass_card("s09-pass", 1, 600)
SCENES[9] = dict(
    body=f"""
<svg class="nw-abs" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">
  <rect width="1920" height="1080" fill="#F6EBDA"/><rect y="930" width="1920" height="150" fill="#EFE2CC"/>
  <g fill="#F4A12B"><circle cx="200" cy="120" r="20"/><circle cx="500" cy="120" r="20"/><circle cx="800" cy="120" r="20"/></g>
  <rect x="80" y="760" width="1000" height="26" rx="10" fill="#B9773E"/><rect x="560" y="786" width="40" height="144" fill="#8E5A2C"/>
  <rect x="520" y="732" width="40" height="28" rx="6" fill="#FBF5EC"/>
</svg>
<div class="nw-chip nw-abs" id="s09-day" style="left:110px;top:80px;background:#141A33;color:#FBF5EC">VIERNES · 20:30</div>
<div class="nw-abs" id="s09-group" style="left:140px;top:250px;display:flex;align-items:flex-end;gap:30px">
  <div id="s09-f1">{friend("s09-a", "#8C5A3C", "#06A77D", "#2B2A3A")}</div>
  <div id="s09-l">{lucia("s09-lu")}</div>
  <div id="s09-f2">{friend("s09-b", "#F0C9A8", "#E85D75", "#B9773E")}</div>
</div>
<div class="nw-abs" id="s09-phone" style="left:508px;top:640px;width:70px;height:120px;border-radius:14px;background:#0E1222"></div>
<div class="nw-abs" id="s09-rings" style="left:470px;top:650px;width:150px;height:150px"><div class="s09-ring"></div><div class="s09-ring"></div></div>
<div class="nw-abs" id="s09-passwrap" style="left:1140px;top:170px">{S09_PASS}</div>
<p class="nw-h nw-abs" id="s09-t1" style="left:1140px;top:730px;font-size:88px;white-space:nowrap">¡Sello <span class="nw-blue">sumado!</span></p>
<p class="nw-abs" id="s09-t2" style="left:1146px;top:850px;font-size:40px;font-weight:700;color:#5B6178">Llevas 2 de 5</p>
""",
    css="""
#s09-passwrap .nw-pass { position: relative; }
#s09-group svg { display: block; }
#s09 .s09-ring { position: absolute; inset: 0; border-radius: 50%; border: 7px solid #1F5EFF; opacity: 0; }
""",
    js="""
  tl.fromTo(S("#s09-day"), { y: -30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }, IN);
  tl.fromTo(S("#s09-group"), { x: -900 }, { x: 0, duration: 1.7, ease: "power2.out" }, 0.3);
  tl.fromTo(S("#s09-group"), { y: 0 }, { y: -12, duration: 0.26, yoyo: true, repeat: 5, ease: "sine.inOut" }, 0.3);
  tl.fromTo(S("#s09-f1"), { scale: 0.9 }, { scale: 1, duration: 0.35, ease: "back.out(2)" }, 2.1);
  tl.fromTo(S("#s09-f2"), { scale: 0.9 }, { scale: 1, duration: 0.35, ease: "back.out(2)" }, 2.25);
  // Tap on the table tag.
  tl.fromTo(S("#s09-phone"), { y: -300, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 2.7);
  gsap.utils.toArray(S(".s09-ring")).forEach((r, i) => {
    tl.fromTo(r, { scale: 0.3, opacity: 0.9 }, { scale: 1.8, opacity: 0, duration: 0.7, ease: "power2.out" }, 3.1 + i * 0.16);
  });
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
SCENES[11] = dict(
    body=f"""
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
    css="#s11-passwrap .nw-pass { position: relative; } #s11-reward { display: inline-block; }",
    js="""
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
SCENES[15] = dict(
    body=f"""
<div class="nw-glow" id="s15-glow" style="width:1500px;height:1500px;left:210px;top:-560px"></div>
<div class="nw-abs" style="left:0;right:0;top:250px;display:flex;align-items:center;justify-content:center;gap:40px">
  <div id="s15-icon" style="width:190px;height:190px;border-radius:46px;background:#1F5EFF;display:grid;place-items:center">{NFC_WAVES("#fff", 120, 6)}</div>
  <div class="nw-h" id="s15-word" style="font-size:180px">NFC Wallet</div>
</div>
<p class="nw-h nw-abs" id="s15-claim" style="left:0;right:0;top:530px;text-align:center;font-size:92px">Tus clientes vuelven <span class="nw-blue">solos.</span></p>
<p class="nw-abs" id="s15-price" style="left:0;right:0;top:680px;text-align:center;font-size:44px;font-weight:700">Desde 29 €/mes por restaurante · 14 días gratis</p>
<div class="nw-abs" id="s15-url" style="left:0;right:0;top:790px;display:flex;justify-content:center"><span class="nw-btn" id="s15-btn" style="background:#1F5EFF;font-size:52px;padding:26px 70px">nfcwallet.es</span></div>
""",
    css="#s15-icon path { stroke-dasharray: 60; }",
    js="""
  tl.fromTo(S("#s15-icon"), { scale: 0, rotation: -20 }, { scale: 1, rotation: 0, duration: 0.5, ease: "power3.out" }, IN);
  tl.fromTo(S("#s15-icon path"), { strokeDashoffset: 60 }, { strokeDashoffset: 0, duration: 0.5, ease: "power2.out", stagger: 0.12 }, 0.45);
  tl.fromTo(S("#s15-word"), { x: -80, opacity: 0, scale: 1.08, transformOrigin: "0% 50%" }, { x: 0, opacity: 1, scale: 1, duration: 0.6, ease: "expo.out" }, 0.5);
  tl.fromTo(S("#s15-claim"), { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "power4.out" }, 1.2);
  tl.fromTo(S("#s15-price"), { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 3.0);
  tl.fromTo(S("#s15-url"), { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.8)" }, 4.3);
  tl.fromTo(S("#s15-btn"), { boxShadow: "0 0 0 0px rgba(31,94,255,.35)" }, { boxShadow: "0 0 0 26px rgba(31,94,255,0)", duration: 1.1, ease: "power2.out", repeat: 4 }, 5.0);
  breath("#s15-glow", 0, 2.6, { scale: 1.1 });
""")


# ---------------------------------------------------------------- pace beats
# Extra beats that fill the holds flagged by the animation map (no dead zone > 1 s).
EXTRA = {
    2: dict(body="""
<div class="nw-abs" id="s02-mesa" style="left:1560px;top:500px"><span class="nw-chip" style="background:#141A33;color:#FBF5EC">Mesa 4</span></div>
<div class="nw-abs" id="s02-rings" style="left:1480px;top:600px;width:120px;height:120px"><div class="s02-ring"></div><div class="s02-ring"></div></div>
""", css="#s02 .s02-ring { position: absolute; inset: 0; border-radius: 50%; border: 6px solid #1F5EFF; opacity: 0; }", js="""
  tl.fromTo(S("#s02-mesa"), { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "back.out(2)" }, 5.4);
  gsap.utils.toArray(S(".s02-ring")).forEach((r, i) => {
    tl.fromTo(r, { scale: 0.3, opacity: 0.9 }, { scale: 1.8, opacity: 0, duration: 0.8, ease: "power2.out", repeat: 2, repeatDelay: 0.1 }, 5.9 + i * 0.25);
  });
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
  tl.fromTo(S("#s05-door svg rect:nth-of-type(1)"), { scaleX: 1 }, { scaleX: 0.15, duration: 0.4, ease: "power3.in", transformOrigin: "100% 50%" }, 6.7);
  tl.fromTo(S("#s05-door"), { rotation: 0 }, { rotation: -1.2, duration: 0.08, yoyo: true, repeat: 3, ease: "sine.inOut" }, 7.1);
  tl.fromTo(S("#s05-title"), { scale: 1 }, { scale: 1.06, duration: 0.25, yoyo: true, repeat: 1, ease: "power2.out", transformOrigin: "0% 50%" }, 7.6);
"""),
    7: dict(body="""<p class="nw-h nw-abs" id="s07-done" style="left:110px;top:910px;font-size:96px;white-space:nowrap">Dos clics. <span class="nw-blue">Listo.</span></p>""",
            css="", js="""
  tl.fromTo(S("#s07-label"), { x: 60, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 1.5);
  tl.fromTo(S("#s07-done"), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.42, ease: "power4.out" }, 11.2);
  tl.fromTo(S("#s07-paco .paco-arm"), { rotation: -150 }, { rotation: -120, duration: 0.25, yoyo: true, repeat: 5, ease: "sine.inOut", immediateRender: false }, 12.0);
"""),
    9: dict(body="""
<p class="nw-abs" id="s09-t3" style="left:1146px;top:920px;font-size:40px;font-weight:800;color:#1F5EFF">Ha vuelto gracias a tu promo.</p>
<div class="nw-abs" id="s09-cheers" style="left:890px;top:640px;display:flex;gap:6px">
  <div id="s09-g1">""" + BEER_SVG.format(s=110) + """</div><div id="s09-g2" style="transform:scaleX(-1)">""" + BEER_SVG.format(s=110) + """</div>
</div>
""", css="", js="""
  tl.fromTo(S("#s09-cheers"), { y: 120, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 4.6);
  tl.fromTo(S("#s09-g1"), { rotation: 0 }, { rotation: 14, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out", transformOrigin: "50% 100%" }, 5.2);
  tl.fromTo(S("#s09-g2"), { rotation: 0 }, { rotation: -14, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out", transformOrigin: "50% 100%" }, 5.2);
  tl.fromTo(S("#s09-t3"), { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 6.1);
  tl.fromTo(S("#s09-group"), { scale: 1 }, { scale: 1.04, duration: 2.6, ease: "sine.inOut", transformOrigin: "50% 100%" }, 7.0);
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
VO_OFFSET = {n: (TIN[n][1] + 0.1 if TIN[n][0] != "none" else 0.1) for n in range(1, 16)}
VO_OFFSET[1] = 0.1
# Scene-local SFX cues: (scene, local time, file, volume)
SFX = [
    (1, 1.42, "impact-bass-1", 0.32),
    (2, 4.6, "pop", 0.45),
    (3, 2.55, "sparkle", 0.45), (3, 2.15, "whoosh-short", 0.35),
    (4, 1.1, "click", 0.7), (4, 1.75, "whoosh-short", 0.4),
    (5, 0.6, "pop", 0.55), (5, 1.55, "click", 0.35), (5, 1.97, "click", 0.35), (5, 2.39, "click", 0.35),
    (6, 0.35, "riser", 0.16),
    (7, 2.9, "typing", 0.45), (7, 5.55, "click", 0.8), (7, 6.45, "click", 0.8), (7, 6.9, "chime", 0.45),
    (8, 1.6, "notification", 0.8),
    (9, 3.1, "sparkle", 0.4), (9, 3.4, "pop", 0.55),
    (11, 1.95, "pop", 0.4), (11, 3.6, "sparkle", 0.45), (11, 6.3, "click", 0.7), (11, 6.5, "chime", 0.4),
    (12, 1.62, "click", 0.7),
    (13, 1.55, "click", 0.8), (13, 2.05, "click", 0.8), (13, 3.15, "sparkle", 0.45),
    (14, 0.6, "pop", 0.35), (14, 2.1, "pop", 0.35), (14, 3.5, "pop", 0.35), (14, 5.6, "pop", 0.35),
    (15, 0.45, "sparkle", 0.45), (15, 4.3, "pop", 0.5),
]


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
            sfx_file = "whoosh" if kind == "whip" else "whoosh-short"
            audio.append(f'      <audio id="sfx-tr-{sid}" src="assets/sfx/{sfx_file}.mp3" data-start="{max(0, start - 0.05):.3f}" data-duration="0.57" data-track-index="13" data-volume="0.35" data-audio-group="sfx"></audio>')

    vo_windows = []
    for n in range(1, 16):
        start, dur, ov = slot(n)
        f = ROOT / "assets" / "voice" / f"vo-{n:02d}.wav"
        length = round(wav_len(f), 3)
        t0 = round(start + VO_OFFSET[n], 3)
        assert t0 + length <= start + dur + 1e-6, f"voice {n} overruns its scene"
        vo_windows.append((t0, t0 + length))
        audio.append(f'      <audio id="vo-{n:02d}" src="assets/voice/vo-{n:02d}.wav" data-start="{t0}" '
                     f'data-duration="{length}" data-track-index="11" data-volume="1" data-audio-group="voiceover"></audio>')

    lanes_end = {12: -1.0, 14: -1.0, 15: -1.0}  # SFX tracks: first free lane, no overlaps per track
    for i, (n, t, name, vol) in sorted(enumerate(SFX), key=lambda x: slot(x[1][0])[0] + x[1][1]):
        start, dur, ov = slot(n)
        f = ROOT / "assets" / "sfx" / f"{name}.mp3"
        t0 = round(start + t, 3)
        length = round(min(wav_len(f), start + dur - t0), 3)
        track = next(k for k, end in lanes_end.items() if end <= t0)
        lanes_end[track] = t0 + length
        audio.append(f'      <audio id="sfx-{i:02d}" src="assets/sfx/{name}.mp3" data-start="{t0}" '
                     f'data-duration="{length}" data-track-index="{track}" data-volume="{vol}" data-audio-group="sfx"></audio>')

    # Music bed. Ducking under the voice is done by the carve (EQ dips + level
    # envelope) run after the index is written; here only the bed itself.
    VOICE_CHAIN = {"version": 1, "nodes": [
        {"type": "highpass", "id": "v1", "params": {"frequency": 90, "q": 0.707}},
        {"type": "peaking", "id": "v2", "params": {"frequency": 320, "gain": -3, "q": 1.2}},
        {"type": "compressor", "id": "v3", "params": {"threshold": -24, "ratio": 3, "attack": 8, "release": 160, "makeup": 4}},
        {"type": "peaking", "id": "v4", "params": {"frequency": 3200, "gain": 3, "q": 0.9}},
        {"type": "limiter", "id": "v5", "params": {"limit": -1.5, "attack": 2, "release": 60}}]}
    SFX_CHAIN = {"version": 1, "nodes": [
        {"type": "compressor", "id": "s1", "params": {"threshold": -18, "ratio": 4, "attack": 2, "release": 120}},
        {"type": "limiter", "id": "s2", "params": {"limit": -6, "attack": 1, "release": 80}}]}
    def bus(gid, label, vol, chain):
        return (f'      <hf-audio-group id="{gid}" data-label="{label}" data-volume="{vol}" '
                f"data-fx-chain='{json.dumps(chain, separators=(',', ':'))}'></hf-audio-group>")
    audio.insert(0, bus("sfx", "Efectos", 0.8, SFX_CHAIN))
    audio.insert(0, bus("voiceover", "Voz en off", 1.0, VOICE_CHAIN))
    audio.insert(0, f'      <audio id="bgm" src="assets/music/bed-v2.wav" data-start="0" data-duration="{TOTAL}" '
                    f'data-track-index="10" data-volume="0.6" data-audio-group="music"></audio>')

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
    carve_and_fade()
    print("built", len(SCENES), "scenes;", len(audio), "audio clips; total", TOTAL, "s")


def carve_and_fade():
    """Voice-over carve on the bed, then fold a fade-in/out volume lane into its automation."""
    import html
    import os
    import re
    carve = pathlib.Path(os.path.expanduser("~/.claude/skills/hyperframes-audio/scripts/carve.mjs"))
    subprocess.run(["node", str(carve), "--comp", "index.html", "--strength", "0.5"], cwd=ROOT, check=True, capture_output=True)
    path = ROOT / "index.html"
    src = path.read_text()
    tag = re.search(r'<audio id="bgm"[^>]*>', src).group(0)
    m = re.search(r'data-automation=("([^"]*)"|\'([^\']*)\')', tag)
    auto = json.loads(html.unescape(m.group(2) or m.group(3))) if m else {"version": 1, "lanes": []}
    auto["lanes"] = [l for l in auto["lanes"] if l["target"] != "volume"]
    auto["lanes"].insert(0, {"target": "volume", "points": [
        {"t": 0, "v": 0}, {"t": 0.4, "v": 1}, {"t": TOTAL - 2.0, "v": 1}, {"t": TOTAL, "v": 0}]})
    value = html.escape(json.dumps(auto, separators=(",", ":")), quote=True)
    new_tag = (tag.replace(m.group(0), f'data-automation="{value}"') if m
               else tag[:-1] + f' data-automation="{value}">')
    path.write_text(src.replace(tag, new_tag))


if __name__ == "__main__":
    build()
