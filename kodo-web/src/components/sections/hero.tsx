"use client";

import {
  motion,
  useMotionValue,
  useSpring,
  useTransform,
  type MotionValue,
} from "motion/react";
import { useState } from "react";

import { Typewriter } from "@/components/cult/typewriter";
import { DotField } from "@/components/dot-field";
import { cn } from "@/lib/utils";

const layers = [
  ["L0", "Diseño", "ux · ui · design systems"],
  ["L1", "Frontend", "angular · react · vue"],
  ["L2", "Backend", "node · python · apis"],
  ["L3", "Arquitectura", "ddd · eventos · microservicios"],
  ["L4", "Infraestructura", "aws · gcp · azure · k8s"],
  ["L5", "DevOps", "ci/cd · iac · observabilidad"],
  ["L6", "IA aplicada", "rag · agentes · guardrails · evals"],
] as const;

const ease = [0.16, 1, 0.3, 1] as const;

function Slab({
  i,
  code,
  name,
  desc,
  mx,
  active,
  onHover,
}: {
  i: number;
  code: string;
  name: string;
  desc: string;
  mx: MotionValue<number>;
  active: boolean;
  onHover: (i: number | null) => void;
}) {
  const ai = i === layers.length - 1;
  // Cada capa tiene una profundidad distinta: se deslizan como paneles de un fusuma.
  const depth = (i + 1) / layers.length;
  const x = useTransform(mx, (v) => v * 46 * depth);

  return (
    <motion.li
      style={{ x }}
      initial={{ clipPath: "inset(0 0 0 100%)", opacity: 0 }}
      animate={{ clipPath: "inset(0 0 0 0%)", opacity: 1 }}
      transition={{ duration: 1.1, delay: 0.35 + (layers.length - i) * 0.08, ease }}
      onHoverStart={() => onHover(i)}
      onHoverEnd={() => onHover(null)}
      className="list-none"
    >
      <motion.div
        animate={{ x: active ? -28 : 0 }}
        transition={{ type: "spring", stiffness: 260, damping: 26 }}
        className={cn(
          "flex cursor-default items-center justify-between gap-4 rounded-md border px-5 transition-colors duration-300",
          ai
            ? "h-[84px] border-lima bg-lima text-negro shadow-[0_20px_60px_-10px_rgba(172,231,50,0.45)]"
            : "h-[60px] border-blanco/10 bg-azul/80 backdrop-blur-md",
          !ai && active && "border-lima/60 bg-teal/90",
        )}
        style={{ marginLeft: `${(layers.length - 1 - i) * 14}px` }}
      >
        <span className="flex items-center gap-3.5">
          <span className={cn("font-mono text-[11px]", ai ? "text-negro" : "text-lima")}>
            {code}
          </span>
          <span
            className={cn(
              "font-display",
              ai ? "text-[28px] font-semibold" : "text-xl",
            )}
          >
            {name}
          </span>
        </span>
        <span
          className={cn(
            "hidden font-mono text-[11px] sm:block",
            ai ? "text-negro/75" : "text-blanco/50",
          )}
        >
          {desc}
        </span>
      </motion.div>
    </motion.li>
  );
}

export function Hero() {
  const raw = useMotionValue(0);
  const mx = useSpring(raw, { stiffness: 90, damping: 20 });
  const [active, setActive] = useState<number | null>(null);

  return (
    <section
      id="top"
      onPointerMove={(e) => {
        const r = e.currentTarget.getBoundingClientRect();
        raw.set(((e.clientX - r.left) / r.width - 0.5) * 2);
      }}
      onPointerLeave={() => raw.set(0)}
      className="relative isolate min-h-[100svh] overflow-hidden bg-negro"
    >
      <div className="pointer-events-none absolute -right-40 -top-32 -z-10 size-[900px] rounded-full bg-teal/90 blur-[220px]" />
      <div className="pointer-events-none absolute bottom-0 right-40 -z-10 size-[360px] rounded-full bg-lima/30 blur-[180px]" />
      <DotField className="absolute inset-0 -z-10 h-full w-full" />

      <div className="mx-auto grid max-w-[1440px] gap-14 px-4 pb-28 pt-32 md:px-16 lg:grid-cols-[1.05fr_1fr] lg:items-center lg:pt-40">
        <div>
          <motion.a
            href="#contacto"
            initial={{ opacity: 0, y: 10, filter: "blur(6px)" }}
            animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
            transition={{ duration: 0.8, delay: 0.2, ease }}
            className="group inline-flex items-center gap-2.5 rounded-full border border-blanco/12 bg-black px-4 py-2.5 font-mono text-xs text-blanco/85 transition-[padding] duration-500 hover:pr-6"
          >
            <span className="relative flex size-2">
              <span className="absolute inset-0 animate-ping rounded-full bg-lima/70" />
              <span className="relative size-2 rounded-full bg-lima" />
            </span>
            Agenda Q4 2026 · 2 huecos para equipos FDE
            <span className="max-w-0 overflow-hidden text-lima transition-[max-width] duration-500 group-hover:max-w-8">
              →
            </span>
          </motion.a>

          <h1 className="font-display mt-8 text-[18vw] font-extralight leading-[0.92] tracking-[-0.04em] sm:text-[8.6rem] lg:text-[7.2rem] xl:text-[8.4rem]">
            {["Del", "píxel"].map((w, i) => (
              <span key={w} className="inline-block overflow-hidden pr-[0.2em] align-bottom">
                <motion.span
                  className="inline-block"
                  initial={{ y: "110%" }}
                  animate={{ y: 0 }}
                  transition={{ duration: 1, delay: 0.3 + i * 0.08, ease }}
                >
                  {w}
                </motion.span>
              </span>
            ))}
            <br />
            <span className="whitespace-nowrap">
            <span className="inline-block overflow-hidden pr-[0.2em] align-bottom">
              <motion.span
                className="inline-block"
                initial={{ y: "110%" }}
                animate={{ y: 0 }}
                transition={{ duration: 1, delay: 0.46, ease }}
              >
                al
              </motion.span>
            </span>
            <span className="inline-block overflow-hidden align-bottom">
              <motion.span
                className="inline-block font-semibold tracking-[-0.05em] text-lima"
                initial={{ y: "110%" }}
                animate={{ y: 0 }}
                transition={{ duration: 1, delay: 0.54, ease }}
              >
                modelo.
              </motion.span>
            </span>
            </span>
          </h1>

          <motion.p
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.9, delay: 0.8, ease }}
            className="mt-8 max-w-[560px] text-lg font-light leading-relaxed text-blanco/78 md:text-xl"
          >
            Diseñamos, desarrollamos, arquitecturamos, desplegamos y operamos
            software. Y cuando llega la IA, nos sentamos dentro de tu equipo como{" "}
            <em className="not-italic text-blanco">forward deployed engineers</em>{" "}
            hasta que funciona en producción.
          </motion.p>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.1 }}
            className="mt-6 min-h-6 font-mono text-[15px] text-blanco/90"
          >
            <span className="mr-2 text-lima">&gt;</span>
            <Typewriter
              delay={1.2}
              baseText="y luego "
              texts={[
                "lo ponemos en producción.",
                "lo medimos con evals.",
                "le ponemos guardrails.",
                "desaparecemos. El sistema se queda.",
              ]}
            />
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.9, delay: 1, ease }}
            className="mt-10 flex flex-wrap gap-4"
          >
            <a
              href="#contacto"
              className="rounded-[14px] bg-lima px-7 py-4 text-base text-negro shadow-[inset_0_1px_0_rgba(255,255,255,0.45),0_8px_30px_-6px_rgba(172,231,50,0.35)] transition-transform hover:-translate-y-0.5"
            >
              Reserva una llamada
            </a>
            <a
              href="#proyectos"
              className="rounded-[14px] border border-blanco/18 bg-blanco/[0.04] px-7 py-4 text-base transition-colors hover:border-blanco/40"
            >
              Ver proyectos →
            </a>
          </motion.div>
        </div>

        <div className="relative">
          <ul className="flex flex-col gap-3.5" aria-label="Las siete capas que cubrimos">
            {layers.map(([code, name, desc], i) => (
              <Slab
                key={code}
                i={i}
                code={code}
                name={name}
                desc={desc}
                mx={mx}
                active={active === i}
                onHover={setActive}
              />
            ))}
          </ul>
          <p className="mt-6 hidden font-mono text-[11px] text-blanco/40 md:block">
            ↑ mueve el ratón: las capas se deslizan como un fusuma
          </p>
        </div>
      </div>

      <div className="absolute inset-x-0 bottom-0 border-t border-blanco/10">
        <div className="mx-auto flex max-w-[1440px] items-center justify-between px-4 py-3.5 font-mono text-[11px] uppercase tracking-[0.08em] text-blanco/45 md:px-16">
          <span>28.0973° N, 15.4660° W — Las Palmas</span>
          <span className="hidden md:inline">Est. Kodo 360</span>
          <span className="hidden md:inline">Diseño → Producción → IA</span>
          <span>Scroll ↓</span>
        </div>
      </div>
    </section>
  );
}
