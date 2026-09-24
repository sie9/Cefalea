# Kodo 360 — web 2026

Nueva web de Kodo 360: **del píxel al modelo**. Un solo equipo para diseño,
desarrollo, arquitectura de software, infraestructura, DevOps e IA aplicada
(forward deployed engineering: RAG, agentes, guardrails, evals).

- Diseño en Figma: https://www.figma.com/design/4cWO3Y3GA86f8xNuWU6uTO
- Paleta original de kodo-360.com: `#141414` `#022127` `#04424e` `#91d600` `#ace732` `#fffcff` `#f5f5f5`
- Tipografías: Raleway (titulares) · Roboto (texto) · Roboto Mono (detalles técnicos)

## Stack

Next.js 16 (App Router) · Tailwind CSS 4 · motion · Lenis.

Componentes de terceros (copiados y adaptados a la paleta):

| Sección | Componente |
| --- | --- |
| Hero — typewriter | Cult UI `typewriter` |
| IA · FDE — terminal | Cult UI `terminal-animation` |
| Método — pestañas | Cult UI `direction-aware-tabs` |
| Contacto — botón | Cult UI `texture-button` (variante `lima`) |
| Nav / contacto — hover | Skiper UI `skiper58` text roll |
| Manifiesto | Skiper UI `skiper31` text scroll |
| Servicios — línea | Skiper UI `skiper19` SVG follow scroll |
| Proyectos | Skiper UI `skiper16` card stack |
| Enlaces | Skiper UI `skiper40` css link |
| Números | NumberFlow (base de `skiper37`) |

Piezas propias: campo de puntos "dither" en canvas que reacciona al cursor,
capas del stack que se deslizan con parallax como un *fusuma*, puertas
correderas que se abren con el scroll en el contacto y wordmark 3D en el footer.

Skiper UI (versión gratuita) exige atribución: está en el footer.

## Desarrollo

```bash
npm install
npm run dev    # http://localhost:3000
npm run build
npm run lint
```
