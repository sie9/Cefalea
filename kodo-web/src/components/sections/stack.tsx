"use client";

import { motion, useScroll } from "motion/react";
import { useRef } from "react";

import { LinePath } from "@/components/skiper/line-path";
import { cn } from "@/lib/utils";

const items = [
  ["01", "Diseño UI/UX", "Investigación, prototipos y design systems en Figma que el equipo de desarrollo consume como tokens, no como capturas.", ["Figma", "Design tokens", "Accesibilidad"]],
  ["02", "Desarrollo Frontend", "Interfaces rápidas y accesibles con Angular, React y Vue, y apps híbridas o nativas con Ionic, Capacitor y Flutter.", ["Angular", "React", "Ionic", "Flutter"]],
  ["03", "Desarrollo Backend", "APIs escalables y lógica de negocio sólida en Node.js y Python. Integraciones con hardware, SDKs y sistemas legados.", ["Node.js", "Python", "GraphQL", "IoT"]],
  ["04", "Arquitectura de software", "Dominios, eventos y microservicios. Decidimos qué no construir antes de construirlo.", ["DDD", "Event-driven", "Microservicios"]],
  ["05", "Infraestructura cloud", "Entornos seguros y escalables en AWS, GCP y Azure. Infraestructura como código desde el primer día.", ["AWS", "GCP", "Azure", "Terraform"]],
  ["06", "DevOps & Plataforma", "CI/CD, Kubernetes, observabilidad y SRE. Desplegar un viernes debería ser aburrido.", ["Kubernetes", "Docker", "CI/CD", "OpenTelemetry"]],
  ["07", "IA aplicada & FDE", "RAG, agentes, guardrails y evals, integrados en tus procesos reales por ingenieros que se incrustan en tu equipo.", ["RAG", "Agentes", "Guardrails", "Evals"]],
] as const;

export function Stack() {
  const ref = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start 0.8", "end 0.9"],
  });

  return (
    <section id="servicios" ref={ref} className="relative overflow-hidden bg-azul">
      <div className="mx-auto grid max-w-[1440px] gap-16 px-4 py-28 md:px-16 md:py-36 lg:grid-cols-[1fr_1.1fr]">
        <div className="relative">
          <div className="lg:sticky lg:top-32">
            <p className="font-mono text-xs uppercase tracking-[0.1em] text-lima">03 — Servicios</p>
            <h2 className="font-display mt-6 text-5xl font-extralight leading-[1.02] tracking-[-0.03em] md:text-7xl">
              Un solo equipo.
              <br />
              Siete capas.
              <br />
              Cero traspasos.
            </h2>
            <p className="mt-6 max-w-[460px] text-lg font-light leading-relaxed text-blanco/70">
              Cada traspaso entre proveedores pierde contexto. Nosotros cubrimos
              todo el stack, así que la decisión de diseño de la semana 1 sigue
              teniendo sentido en el cluster de la semana 40.
            </p>
          </div>
          <LinePath
            progress={scrollYProgress}
            className="pointer-events-none absolute left-0 top-[420px] hidden h-[calc(100%-380px)] w-[92%] lg:block"
          />
        </div>

        <ol className="relative">
          {items.map(([n, title, desc, chips], i) => {
            const ai = i === items.length - 1;
            return (
              <motion.li
                key={n}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: "-15% 0px" }}
                transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
                className={cn(
                  "group flex gap-6 py-9 md:gap-8",
                  ai
                    ? "mt-4 rounded-[20px] bg-lima px-7 text-negro"
                    : "border-t border-blanco/12",
                )}
              >
                <span
                  className={cn(
                    "font-display text-5xl font-extralight leading-none tracking-[-0.04em] transition-transform duration-500 group-hover:-translate-y-1 md:text-6xl",
                    ai ? "text-negro" : "text-lima",
                  )}
                >
                  {n}
                </span>
                <div className="flex flex-col gap-3">
                  <h3 className={cn("font-display text-2xl tracking-tight md:text-3xl", ai && "font-semibold")}>
                    {title}
                  </h3>
                  <p className={cn("max-w-[480px] font-light leading-relaxed", ai ? "text-negro/85" : "text-blanco/65")}>
                    {desc}
                  </p>
                  <ul className="flex flex-wrap gap-2">
                    {chips.map((c) => (
                      <li
                        key={c}
                        className={cn(
                          "rounded-full border px-2.5 py-1 font-mono text-[11px]",
                          ai ? "border-negro/40" : "border-blanco/20 text-blanco/85",
                        )}
                      >
                        {c}
                      </li>
                    ))}
                  </ul>
                </div>
              </motion.li>
            );
          })}
        </ol>
      </div>
    </section>
  );
}
