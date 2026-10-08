# NFC Wallet promo — design spec

## Palette (by role)

| Role                | Hex       | Source                                                        |
| ------------------- | --------- | ------------------------------------------------------------- |
| Background (canvas) | `#FBF5EC` | Warm cream for hospitality; same on every scene               |
| Foreground (text)   | `#141A33` | Night blue, tinted toward the accent                          |
| Accent (focal)      | `#1F5EFF` | NFC Wallet panel primary (`packages/web/ui` `--primary`)      |
| Muted text          | `#5B6178` | Tinted neutral                                                |
| Illustration warm   | `#F4A12B` | Bar lights, wood, drinks — illustration only, never for text  |
| Illustration wood   | `#B9773E` | Tables, bar counter                                           |
| Pepito card bg      | `#1F2937` | Product default pass `backgroundColor`                        |
| Pepito card fg      | `#FFFFFF` | Product default pass `foregroundColor`                        |
| Success             | `#1B7F3B` | Panel `--success` (stamp added, reward redeemed)              |

## Type

- Display: **Archivo Black** 400 (`assets/fonts/archivo-black-400.woff2`) — headlines 88–200px.
- Text: **Montserrat** 500/700/800 (`assets/fonts/montserrat-var.woff2`) — body 32–44px, labels 22–26px.
- Numbers: Montserrat 800 `tabular-nums`.

## Shapes and motion

- Radii: cards 28px, phone 64px, buttons 999px.
- Borders 3px on light canvas; shadows soft and large (`0 30px 60px rgba(20,26,51,.18)`).
- Eases: `expo.out` for entrances, `back.out(1.6)` for pops, `power3.inOut` for camera/pushes.
- Transitions: leftward push/whip only, ≤ 0.4 s, cut on the music beat.

## Illustration

Flat 2D, no outlines, 3–4 tones per object. Lucía: short dark hair `#2B2A3A`, mustard jacket `#F4A12B`, skin `#E8B48F`. Paco: bald, beard `#3B2A20`, apron `#1F5EFF`, skin `#C98B62`.

## Don't

Gradient text, neon, purple-blue gradients, invented product features, static end card, slideshow beats, decorative motion that says nothing.
