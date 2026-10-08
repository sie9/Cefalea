# v3 — personas reales generadas por IA y música nueva

Petición del usuario (literal): «quiero que quites todo el audio del nuevo video y generes música nueva libre de licencias y crees con personas reales (hechas con IA) el video».

Requiere `GEMINI_API_KEY` en el entorno (se lee al empezar la sesión). Comprobar con
`[ -n "$GEMINI_API_KEY" ] && echo ok` antes de nada.

## Decisiones confirmadas

- **Audio:** se quita todo lo anterior (voz en off Kokoro, efectos y música MusicGen). Solo música nueva generada con **Google Lyria** (`media-use/audio/scripts/lyria-recipe.py`), electro pop rápido ~128-140 bpm, 137 s.
  Si el usuario quiere volver a tener voz, ofrecer Gemini TTS en español (no incluido en esta petición).
- **Imagen:** fotos fotorrealistas generadas con el modelo de imagen de Gemini, con movimientos de cámara (Ken Burns, paneos, punch-ins) y cortes rápidos. Sin clips de vídeo.
- **Personajes consistentes:** primero se genera una hoja de referencia de cada personaje y se reutiliza como imagen de referencia en cada plano (campo `refs` de `shots.json`; `tools/gen_images.py --shots` las adjunta).
- Se mantienen encima de las fotos las pantallas del producto recreadas en HTML (landing de la tag, Wallet, panel de Mensajes, tarjeta de fidelidad, notificación) y los textos de la v2.
- Sin narración, el mensaje lo llevan los textos en pantalla: revisar que cada escena tenga su titular (los de `STORYBOARD.md`).

## Pasos

0. Preparar el contenedor nuevo (las herramientas no se guardan entre sesiones):
   `apt-get update && apt-get install -y ffmpeg`, `npx -y hyperframes@0.8.140 skills update general-video`
   (instala la skill `hyperframes` y las de dominio), `npx -y hyperframes@0.8.140 telemetry disable`,
   `uv venv ~/.venvs/hf-audio && VIRTUAL_ENV=~/.venvs/hf-audio uv pip install google-genai numpy soundfile`,
   y `npm i` dentro de `videos/nfc-wallet-promo` (para `@hyperframes/core`, que usa el carve).

1. `python3 tools/gen_images.py --list-models` → elegir el modelo de imagen disponible (p. ej. `gemini-2.5-flash-image` o el más reciente).
2. Generar las hojas de personaje (`shots.json` → `characters`) y enseñárselas al usuario antes de seguir.
3. Generar los planos (`shots.json` → `shots`) en 16:9 → `assets/photos/`.
4. Música: `~/.venvs/hf-audio/bin/python -I ~/.claude/skills/media-use/audio/scripts/lyria-recipe.py --output assets/music/lyria.wav --duration 137 --bpm 132 --brightness 0.8 --density 0.7 --prompt "<ver shots.json music.prompt>"`.
5. `tools/build.py`: sustituir las ilustraciones SVG por las fotos (capa de fondo con Ken Burns) en S02, S03, S05, S07, S08, S09, S11; quitar `vo-*`, `sfx-*` y `bgm`; añadir la música de Lyria con fundidos; re-ajustar los cortes al beat (`npx hyperframes beats .`).
6. `npx hyperframes check`, snapshots, preview, render 16:9 y masterizado a −14 LUFS (ver comandos en el historial de la v2: `loudnorm` + `alimiter` al final).

## Licencia de la música

La música generada con Lyria a través de la API de Gemini no usa obras de terceros; según los términos de Google, el contenido generado pertenece a quien lo genera (lleva marca de agua SynthID). Indicarlo así al usuario, sin prometer más de lo que dicen los términos vigentes.

## Estado (8 oct 2026)

Hecho: pasos 0-6. Máster en `renders/nfc-wallet-v3-16x9-master.mp4` (no versionado).

- Imagen: `gemini-2.5-flash-image` (el Pro daba 503 por demanda). Las referencias de personaje se mandan como JPEG de 768 px
  (los PNG enteros provocaban errores 500); los planos se guardan en JPEG porque los PNG pasan del límite de 2 MB del bundler.
- Fotos en S02, S03, S05, S07, S08, S09, S11 y S15; sin narración, cada escena lleva su titular en pantalla.
- Cortes reajustados al beat más fuerte a ±0,35 s de los de la v2 sobre `lyria.wav`.
- Masterizado (el `loudnorm` lineal no cabía: subir +6,4 dB con −1,3 dBTP de pico):
  ```
  ffmpeg -i renders/nfc-wallet-v3-16x9.mp4 -af "volume=6.8dB,aresample=192000,alimiter=limit=0.75:level=false:attack=1:release=60,aresample=48000" -c:a pcm_s16le t.wav
  ffmpeg -i renders/nfc-wallet-v3-16x9.mp4 -i t.wav -map 0:v -map 1:a -c:v copy -c:a aac -aac_coder twoloop -b:a 256k -movflags +faststart renders/nfc-wallet-v3-16x9-master.mp4
  ```
  Resultado: −14,1 LUFS, −1,7 dBTP. El codificador AAC por defecto (`fast`) subía el pico a +0,8 dBTP; `twoloop` no.

Pendiente: versión 9:16.
