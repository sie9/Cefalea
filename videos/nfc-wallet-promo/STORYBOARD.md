---
format: 1920x1080
duration: 135s
message: "Tus clientes vuelven solos: un toque en la mesa, tu tarjeta en su Wallet y promociones en dos clics"
arc: Hook → Primera visita → El tiempo pasa → Promo en dos clics → Vuelve → Funcionalidades → CTA
audience: dueños de bares y restaurantes en España
mode: collaborative
---

# NFC Wallet — vídeo promocional (v1)

## Decisiones

- **Mensaje:** Tus clientes vuelven solos: un toque en la mesa, tu tarjeta en su Wallet y promociones en dos clics.
- **Audiencia y arco:** dueños de bares y restaurantes. Historia de Lucía (clienta) y Paco (dueño): primera visita → el tiempo pasa → Paco manda una promo → Lucía vuelve; después, ráfaga de funcionalidades y CTA.
- **Formato:** 1920×1080, ~135 s, voz en off (Kokoro `em_alex`, ×1.1), música electro pop ~140 bpm generada con MusicGen; cortes al compás. Versión 9:16 tras aprobar el máster.
- **Hilo conductor (spine):** el móvil de Lucía. Aparece en la mesa (F03), recibe la tarjeta (F04), la notificación (F08) y el sello de vuelta (F09); vuelve como prop en F11–F13.
- **Marca:** fondo crema #FBF5EC (cálido, hostelería), texto azul noche #141A33, acento azul NFC Wallet #1F5EFF (el del panel), apoyo ámbar #F4A12B solo en la ilustración del bar. Tipos: Archivo Black (titulares), Montserrat 500/700 (texto). Tarjeta de Pepito: fondo #1F2937, texto blanco (valores por defecto del producto).
- **Estilo:** ilustración 2D plana (SVG) para personas y escenarios; pantallas del producto recreadas fielmente desde el código (landing de la tag, Wallet, panel de Mensajes).
- **Prohibido:** gradientes en texto, neón, tarjetas idénticas en cuadrícula sin jerarquía, funcionalidades que el producto no tiene, escenas de diapositiva sin movimiento (slideshow) y movimiento que no dice nada (screensaver).
- **Plano sostenido:** F08 — la notificación en la pantalla de bloqueo se queda quieta 1,5 s mientras suena el «ding».
- **Transiciones:** dirección única hacia la izquierda (push/whip a la izquierda), cortes secos al compás; ninguna transición > 0,4 s.
- **Veracidad:** todo lo que se cuenta existe en la plataforma (toque NFC con NTAG 424 DNA, tarjeta Apple/Google Wallet, sellos y premios canjeados por QR del personal, mensajes push con audiencia, avisos de cercanía, estadísticas por mesa, varias cuentas/locales, precio 29 €/mes y 14 días de prueba).

## Frame 1 — Gancho

- scene: "¿Y si tus clientes" / "volvieran" / "SOLOS?" golpean al ritmo
- duration: 6s
- transition_in: cut
- status: built
- src: compositions/01-hook.html
- blueprint: kinetic-type-beats (rules: kinetic-beat-slam)
- voiceover: "¿Y si tus clientes volvieran… solos?"

Tres golpes de texto sobre el crema, la última palabra en azul y enorme. Por qué: plantea el valor en lenguaje del dueño desde el primer segundo.

## Frame 2 — Lucía entra en el bar

- scene: Fachada del "Restaurante Pepito", Lucía entra, se sienta y deja el móvil en la mesa
- duration: 8s
- transition_in: push-left
- status: built
- src: compositions/02-arrive.html
- blueprint: spatial-pan-stations (cámara: puerta → mesa)
- voiceover: "Lucía entra en el Restaurante Pepito. Se sienta… y deja el móvil sobre la mesa."

Por qué: sitúa la historia en el local del cliente objetivo.

## Frame 3 — El toque NFC

- scene: Primer plano de la mesa con la tag "Toca aquí" (logo NFC); el móvil se apoya, ondas NFC, la pantalla se enciende con la página de Pepito
- duration: 10s
- transition_in: cut
- status: built
- src: compositions/03-tap.html
- blueprint: device-surface-showcase
- voiceover: "En cada mesa hay una pequeña tag NFC. Basta un toque… y aparece la tarjeta de Pepito."

Por qué: el gesto clave del producto, tal y como funciona (sin app, sin QR).

## Frame 4 — Añadir a Wallet

- scene: Pantalla del móvil: botón "Añadir a Apple Wallet" pulsado → la tarjeta de Pepito entra en la Wallet
- duration: 9s
- transition_in: cut
- status: built
- src: compositions/04-wallet.html
- blueprint: device-surface-showcase (stepwise flow)
- voiceover: "Un toque más en «Añadir a Wallet». Sin apps. Sin registros. Ya la lleva en el móvil."

Por qué: muestra la fricción cero para el cliente final.

## Frame 5 — Come y se va

- scene: Sello "1/5" en la tarjeta; ráfaga: plato, brindis, cuenta, Lucía sale por la puerta
- duration: 9s
- transition_in: push-left
- status: built
- src: compositions/05-leave.html
- rules: kinetic-beat-slam, stat-bars-and-fills (sello)
- voiceover: "Primer sello. Lucía come, paga… y se va."

## Frame 6 — Pasa el tiempo

- scene: Calendario que pasa hojas a toda velocidad: "3 semanas después"
- duration: 6s
- transition_in: cut
- status: built
- src: compositions/06-time.html
- rules: vertical-spring-ticker
- voiceover: "Pasan los días…"

## Frame 7 — Paco manda una promo en dos clics

- scene: Paco con el portátil; panel NFC Wallet → Mensajes; escribe "2x1 en cañas este viernes"; cursor: clic ① "Todos los clientes", clic ② "Enviar"; contador "Enviado a 318 tarjetas"
- duration: 14s
- transition_in: push-left
- status: built
- src: compositions/07-owner.html
- blueprint: cursor-ui-demo
- voiceover: "Paco, el dueño, abre NFC Wallet. Escribe su promoción: dos por uno en cañas este viernes. Clic… y clic. Enviada a todos sus clientes."

Por qué: el beneficio para el dueño, y la sencillez (dos clics) que pide el guion.

## Frame 8 — La notificación (plano sostenido)

- scene: Pantalla de bloqueo de Lucía: notificación "Restaurante Pepito — 2x1 en cañas este viernes 🍻"
- duration: 8s
- transition_in: whip-left
- status: built
- src: compositions/08-notify.html
- blueprint: device-surface-showcase
- voiceover: "Y en el bolsillo de Lucía… ahí está."

Plano quieto 1,5 s con el «ding». Por qué: el momento de retorno, el corazón del mensaje.

## Frame 9 — Lucía vuelve

- scene: Lucía entra con dos amigos, toca la tag: "¡Sello sumado! Llevas 2 de 5"
- duration: 10s
- transition_in: push-left
- status: built
- src: compositions/09-return.html
- voiceover: "El viernes, Lucía vuelve. Y no viene sola. Toque, sello… y a disfrutar."

Por qué: cierra el círculo: el cliente vuelve gracias a la promo. Callback de F03.

## Frame 10 — Bisagra

- scene: "Y esto es solo el principio."
- duration: 4s
- transition_in: cut
- status: built
- src: compositions/10-hinge.html
- blueprint: kinetic-type-beats
- voiceover: "Y esto es solo el principio."

## Frame 11 — Tarjeta de fidelidad

- scene: La tarjeta se llena de sellos 1→5, "¡Café gratis!"; el camarero escanea el QR de la tarjeta y "Premio canjeado"
- duration: 10s
- transition_in: push-left
- status: built
- src: compositions/11-loyalty.html
- rules: stat-bars-and-fills, counting-dynamic-scale
- voiceover: "Tarjeta de fidelidad: cada visita, un sello. Al completarla, premio. Y el camarero lo canjea escaneando la tarjeta."

## Frame 12 — Tu marca en la Wallet

- scene: Editor de marca del panel a la izquierda; a la derecha la tarjeta en Apple Wallet y Google Wallet cambia de color y logo en directo
- duration: 10s
- transition_in: push-left
- status: built
- src: compositions/12-brand.html
- blueprint: panel-edit-live-sync
- voiceover: "Tu logo, tus colores, tu carta. En Apple Wallet y en Google Wallet, siempre en el móvil de tus clientes."

## Frame 13 — Promoción en dos clics

- scene: "① Escribe ② Envía" con el cursor; decenas de móviles se encienden a la vez
- duration: 9s
- transition_in: push-left
- status: built
- src: compositions/13-two-clicks.html
- blueprint: cta-morph-press
- voiceover: "¿Una promoción? Dos clics. Y llega a todos tus clientes, al instante."

## Frame 14 — Y además

- scene: Se montan seis piezas: "Avisos al pasar cerca", "Estadísticas por mesa", "Todos tus locales en una cuenta", "Tags NFC imposibles de copiar", "Facturas automáticas", "RGPD de serie"
- duration: 11s
- transition_in: push-left
- status: built
- src: compositions/14-features.html
- blueprint: grid-card-assemble
- voiceover: "Avisos cuando pasan cerca. Estadísticas por mesa. Todos tus locales en una sola cuenta. Y tags NFC imposibles de copiar."

## Frame 15 — Cierre

- scene: Logo "NFC Wallet" se ensambla; "Tus clientes vuelven solos." · "Desde 29 €/mes · 14 días gratis" · "nfcwallet.es"
- duration: 11s
- transition_in: whip-left
- status: built
- src: compositions/15-cta.html
- blueprint: logo-assemble-lockup
- voiceover: "NFC Wallet. Tus clientes vuelven solos. Pruébalo gratis catorce días en nfcwallet punto es."
