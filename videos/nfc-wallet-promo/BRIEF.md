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

## Notes

- Sin credenciales de IA en el entorno: el estilo visual pedido (imágenes generadas por IA) no es posible; se usa ilustración 2D plana animada (SVG/HTML) para personas y escenarios, y recreaciones fieles de las pantallas del producto.
- Primera visita contada de forma fiel al producto: toque NFC en la tag de la mesa → página con la marca del restaurante → "Añadir a Wallet". La promoción llega como notificación de la tarjeta de Wallet en la pantalla de bloqueo.
- Marca: "NFC Wallet", azul #1f5eff del panel; restaurante de demo "Restaurante Pepito". Datos reales del producto: desde 29 €/mes por restaurante, 14 días de prueba, kit NFC 49 €, tags NTAG 424 DNA.
- No inventar funcionalidades que el producto no tiene.
