"use client";

import { useEffect, useRef } from "react";

/**
 * Campo de puntos "dither" en canvas: los puntos cercanos al cursor
 * crecen y se desplazan, como si el ratón empujara una tela de píxeles.
 */
export function DotField({ className }: { className?: string }) {
  const ref = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = ref.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const GAP = 22;
    let w = 0;
    let h = 0;
    let raf = 0;
    const mouse = { x: -9999, y: -9999, tx: -9999, ty: -9999 };

    const resize = () => {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = canvas.clientWidth;
      h = canvas.clientHeight;
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };

    const onMove = (e: PointerEvent) => {
      const r = canvas.getBoundingClientRect();
      mouse.tx = e.clientX - r.left;
      mouse.ty = e.clientY - r.top;
    };

    const draw = (t: number) => {
      mouse.x += (mouse.tx - mouse.x) * 0.12;
      mouse.y += (mouse.ty - mouse.y) * 0.12;
      ctx.clearRect(0, 0, w, h);
      const cx = w * 0.72;
      const cy = h * 0.42;
      const R = Math.max(w, h) * 0.45;
      for (let y = GAP / 2; y < h; y += GAP) {
        for (let x = GAP / 2; x < w; x += GAP) {
          const dc = Math.hypot(x - cx, y - cy);
          const base = Math.max(0, 1 - dc / R);
          const wave = reduce ? 0 : Math.sin(x * 0.012 + y * 0.018 - t * 0.0012) * 0.5 + 0.5;
          const dm = Math.hypot(x - mouse.x, y - mouse.y);
          const push = Math.max(0, 1 - dm / 160);
          const a = base * (0.25 + wave * 0.45) + push * 0.9;
          if (a < 0.04) continue;
          const ox = push ? ((x - mouse.x) / (dm || 1)) * push * 10 : 0;
          const oy = push ? ((y - mouse.y) / (dm || 1)) * push * 10 : 0;
          const s = 1.2 + push * 2.6;
          ctx.fillStyle = push > 0.35 ? `rgba(172,231,50,${Math.min(1, a)})` : `rgba(255,252,255,${Math.min(0.55, a * 0.6)})`;
          ctx.fillRect(x + ox - s / 2, y + oy - s / 2, s, s);
        }
      }
      if (!reduce) raf = requestAnimationFrame(draw);
    };

    resize();
    window.addEventListener("resize", resize);
    window.addEventListener("pointermove", onMove);
    raf = requestAnimationFrame(draw);
    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", resize);
      window.removeEventListener("pointermove", onMove);
    };
  }, []);

  return <canvas ref={ref} className={className} aria-hidden />;
}
