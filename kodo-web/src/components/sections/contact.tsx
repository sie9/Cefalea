"use client";

import { motion, useScroll, useTransform, type MotionValue } from "motion/react";
import { useRef } from "react";

import { TextureButton } from "@/components/cult/texture-button";
import { TextRoll } from "@/components/skiper/text-roll";

/** Panel de un fusuma: puerta corredera con su retícula de listones. */
function Door({ side, x }: { side: "left" | "right"; x: MotionValue<string> }) {
  return (
    <motion.div
      aria-hidden
      style={{ x }}
      className={`absolute inset-y-0 z-20 w-1/2 bg-teal ${side === "left" ? "left-0 border-r" : "right-0 border-l"} border-lima/40`}
    >
      <div className="grid h-full grid-cols-4 grid-rows-6">
        {Array.from({ length: 24 }).map((_, i) => (
          <div key={i} className="border-b border-r border-blanco/[0.07]" />
        ))}
      </div>
      <div
        className={`absolute top-1/2 h-24 w-1.5 -translate-y-1/2 rounded-full bg-lima/70 ${side === "left" ? "right-6" : "left-6"}`}
      />
    </motion.div>
  );
}

export function Contact() {
  const ref = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start end", "start start"] });
  const left = useTransform(scrollYProgress, [0.25, 0.95], ["0%", "-100%"]);
  const right = useTransform(scrollYProgress, [0.25, 0.95], ["0%", "100%"]);
  const scale = useTransform(scrollYProgress, [0.3, 1], [0.86, 1]);

  return (
    <section id="contacto" ref={ref} className="relative isolate overflow-hidden bg-negro">
      <Door side="left" x={left} />
      <Door side="right" x={right} />
      <div className="pointer-events-none absolute left-1/2 top-1/2 -z-10 size-[560px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-lima/20 blur-[160px]" />

      <motion.div
        style={{ scale }}
        className="mx-auto flex min-h-[100svh] max-w-[1440px] flex-col items-center justify-center gap-8 px-4 py-28 text-center"
      >
        <p className="font-mono text-xs uppercase tracking-[0.1em] text-lima">07 — Contacto</p>
        <a href="mailto:hola@kodo-360.com" className="block">
          <TextRoll center className="font-display pb-[0.12em] text-[19vw] font-extralight leading-[1.05] tracking-[-0.05em] md:text-[10rem]">
            ¿Hablamos?
          </TextRoll>
        </a>
        <p className="max-w-[420px] text-lg font-light leading-relaxed text-blanco/75">
          Cuéntanos qué quieres construir, o qué quieres que por fin funcione.
          Respondemos en menos de 24&nbsp;h.
        </p>
        <TextureButton
          variant="lima"
          size="lg"
          className="w-auto rounded-[16px]"
          onClick={() => {
            window.location.href = "mailto:hola@kodo-360.com?subject=Quiero%20hablar%20con%20un%20ingeniero";
          }}
        >
          <span className="px-3 py-2 text-base">Reserva 30 min con un ingeniero →</span>
        </TextureButton>
        <p className="font-mono text-[13px] text-blanco/55">o escribe a hola@kodo-360.com</p>
      </motion.div>
    </section>
  );
}
