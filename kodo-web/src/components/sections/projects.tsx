"use client";

import { useScroll } from "motion/react";
import { useRef } from "react";

import { CssLink } from "@/components/skiper/css-link";
import { StickyCard } from "@/components/skiper/sticky-card";
import { cn } from "@/lib/utils";

const cases = [
  {
    client: "HBS",
    title: "Plataforma global de reservas",
    desc: "Tech leads de más de 30 desarrolladores senior frontend. Nueva versión de una herramienta crítica para millones de usuarios, en producción en 6 meses.",
    tags: "Liderazgo técnico · Angular · Arquitectura",
    bg: "bg-teal",
  },
  {
    client: "TMB",
    title: "Updater & Stats i alarmes",
    desc: "Beacons Bluetooth en el metro de Barcelona: plugin Capacitor sobre un SDK solo-Java y detección de caídas para la seguridad de los trabajadores.",
    tags: "Ionic · Capacitor · BLE · Android",
    bg: "bg-azul",
  },
  {
    client: "Worldsensing",
    title: "Testeo automatizado de IoT",
    desc: "SSH, sensores, PLCs y atornilladoras industriales orquestados en un único flujo con informes automáticos e integración con bases de datos globales.",
    tags: "Python · Hardware · Industrial",
    bg: "bg-negro",
  },
  {
    client: "Visor",
    title: "Smart city orientada a datos",
    desc: "Funcionalidades críticas e integraciones con múltiples proveedores para convertir una infraestructura IoT en una plataforma robusta y escalable.",
    tags: "IoT · Integraciones · Escalabilidad",
    bg: "bg-teal",
  },
  {
    client: "Binary",
    title: "Bticket",
    desc: "Escáner óptico y NFC sobre SDKs de distintas PDAs, funcionamiento offline y sincronización para eventos internacionales de alto nivel.",
    tags: "Mobile · Offline-first · NFC",
    bg: "bg-azul",
  },
];

export function Projects() {
  const container = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: container,
    offset: ["start start", "end end"],
  });

  return (
    <section id="proyectos" className="bg-gris text-negro">
      <div className="mx-auto grid max-w-[1440px] gap-10 px-4 md:px-16 lg:grid-cols-[0.9fr_1.1fr]">
        <div className="pt-28 md:pt-36 lg:pb-36">
          <div className="lg:sticky lg:top-36">
            <p className="font-mono text-xs uppercase tracking-[0.1em] text-teal">05 — Proyectos</p>
            <h2 className="font-display mt-6 text-5xl font-extralight leading-[1.02] tracking-[-0.03em] md:text-7xl">
              Software crítico,
              <br />
              en sitios difíciles.
            </h2>
            <p className="mt-6 max-w-[440px] text-lg font-light leading-relaxed text-negro/65">
              Metro de Barcelona, eventos internacionales, IoT industrial, smart
              cities. Algunos de los proyectos en los que hemos estado dentro.
            </p>
            <blockquote className="mt-14 max-w-[500px] border-l-2 border-teal pl-7">
              <p className="font-display text-2xl font-light leading-snug md:text-[1.75rem]">
                “Kodo 360 no solo aporta código, aporta dirección, visión y
                resultados medibles.”
              </p>
              <footer className="mt-4 font-mono text-xs text-teal">
                — HBS · Plataforma global de reservas
              </footer>
            </blockquote>
            <CssLink href="#contacto" className="mt-12 text-base">
              Cuéntanos el tuyo
            </CssLink>
          </div>
        </div>

        <div ref={container} className="relative pb-[30vh] pt-[10vh]">
          {cases.map((c, i) => {
            const targetScale = Math.max(0.6, 1 - (cases.length - i - 1) * 0.06);
            return (
              <StickyCard
                key={c.client}
                i={i}
                progress={scrollYProgress}
                range={[i / cases.length, 1]}
                targetScale={targetScale}
                className={cn(c.bg, "text-blanco shadow-[0_-10px_40px_-10px_rgba(0,13,18,0.28)]")}
              >
                <div className="pointer-events-none absolute -right-24 -top-40 size-[420px] rounded-full bg-lima/18 blur-[120px]" />
                <div className="relative flex h-full flex-col p-8 md:p-10">
                  <div className="flex items-center justify-between font-mono text-xs">
                    <span className="font-medium uppercase tracking-[0.1em] text-lima">{c.client}</span>
                    <span className="text-blanco/50">
                      {String(i + 1).padStart(2, "0")} / {String(cases.length).padStart(2, "0")}
                    </span>
                  </div>
                  <div className="mt-auto">
                    <h3 className="font-display text-3xl font-light tracking-[-0.02em] md:text-[2.75rem] md:leading-[1.05]">
                      {c.title}
                    </h3>
                    <p className="mt-4 max-w-[480px] font-light leading-relaxed text-blanco/72">{c.desc}</p>
                    <p className="mt-4 font-mono text-[11px] text-lima/90">{c.tags}</p>
                  </div>
                </div>
              </StickyCard>
            );
          })}
        </div>
      </div>
    </section>
  );
}
