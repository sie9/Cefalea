---
workflow: general-video
flow: automation
storyboard: yes
message: "Tus clientes vuelven solos: un toque en la mesa, tu tarjeta en su Wallet y promociones en dos clics"
destination: youtube
aspect: 1920x1080
language: es
audience: dueños de bares y restaurantes en España
length: 135s
angle: story
voice: kokoro:em_alex
---

## Intent

Vídeo promocional de NFC Wallet (plataforma NFC + Apple/Google Wallet para restaurantes). Guion del usuario: una persona entra en un bar, apoya su móvil en la mesa (toque NFC), recibe la tarjeta en su Wallet y la acepta, come y se va; pasa el tiempo; el dueño entra en la app y manda una promoción especial; la notificación llega al móvil y el cliente vuelve al restaurante. Después, el resto de funcionalidades: tarjeta de fidelidad, cómo se ve el restaurante en la Wallet del móvil y lo fácil que es mandar una promoción en dos clics.

Tono (palabras del usuario): "muy ágil de velocidad y sencillez", "música muy rápida y transiciones rápidas", "que el vídeo dure 2 minutos como mínimo para explicarlo todo".

## Customizations

- Voz en off sintética en español: Kokoro local, voz `em_alex` (elegida por el usuario tras escuchar muestras), velocidad ≈1.1.
- Música generada por IA en local con MusicGen (facebook/musicgen-small): electro pop rápido (~140 bpm), fragmento semilla en bucle con fundidos; el usuario escuchó una muestra y la aceptó.
- Formatos: máster 16:9 (1920×1080); versión 9:16 (1080×1920) adaptada después de aprobar el máster.

- v2 (mezcla): música reconstruida a partir de los tramos estables de la toma de MusicGen (`tools/make_bed.sh` → `assets/music/bed-v2.wav`), carve 0.5, bus de voz (highpass, de-mud, compresor, presencia, limitador) y bus de efectos con limitador.
- v3 pedida por el usuario: «darle vida» con **personas reales hechas por IA** en lugar de iconos 2D, y mejor audio. Decisiones confirmadas:
  - Proveedor: **Google Gemini** con la clave en la variable de entorno `GEMINI_API_KEY` (nueva sesión).
  - Movimiento: **fotos fotorrealistas generadas por IA con movimientos de cámara** (zoom, paneo, cortes rápidos), no clips de vídeo.
  - Con la clave: imágenes de personas con personajes consistentes (Lucía, sus dos amigos, Paco) usando imagen de referencia; música con Lyria; voz en off natural en español con Gemini TTS.
  - Se mantienen las pantallas del producto (landing de la tag, Wallet, panel de Mensajes, tarjeta de fidelidad) recreadas en HTML encima de las fotos.

- v3 (petición literal): «quiero que quites todo el audio del nuevo video y generes música nueva libre de licencias y crees con personas reales (hechas con IA) el video». Sin voz en off ni efectos: solo música nueva de Lyria. Plan detallado en `PLAN-v3.md`, planos en `shots.json`, generador en `tools/gen_images.py`.

## Notes

- Sin credenciales de IA en el entorno: el estilo visual pedido (imágenes generadas por IA) no es posible; se usa ilustración 2D plana animada (SVG/HTML) para personas y escenarios, y recreaciones fieles de las pantallas del producto.
- Primera visita contada de forma fiel al producto: toque NFC en la tag de la mesa → página con la marca del restaurante → "Añadir a Wallet". La promoción llega como notificación de la tarjeta de Wallet en la pantalla de bloqueo.
- Marca: "NFC Wallet", azul #1f5eff del panel; restaurante de demo "Restaurante Pepito". Datos reales del producto: desde 29 €/mes por restaurante, 14 días de prueba, kit NFC 49 €, tags NTAG 424 DNA.
- No inventar funcionalidades que el producto no tiene.
