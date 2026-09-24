"use client";

import NumberFlow from "@number-flow/react";
import { useInView } from "motion/react";
import { useRef } from "react";

import { DirectionAwareTabs } from "@/components/cult/direction-aware-tabs";

const steps = [
  {
    label: "Incrustarse",
    when: "Semana 1–2",
    title: "Nos sentamos en tu equipo",
    body: "Un pod de 2–4 ingenieros entra en tus rituales, tu Slack y tus repos. Mapeamos procesos, datos y restricciones legales antes de escribir una línea, y salimos con un backlog priorizado por impacto.",
    out: ["Mapa de procesos y datos", "Arquitectura objetivo", "Plan de evals y guardrails", "Primer prototipo en 10 días"],
  },
  {
    label: "Construir",
    when: "Semana 3–8",
    title: "Producto real, no slides",
    body: "Diseño, frontend, backend e IA avanzan juntos en ciclos cortos con usuarios reales. Cada incremento pasa por evals automáticas y revisión de seguridad antes de llegar a nadie.",
    out: ["Design system en código", "APIs y agentes versionados", "Suite de evals propia", "Demo semanal con negocio"],
  },
  {
    label: "Desplegar",
    when: "Semana 8–10",
    title: "A producción sin drama",
    body: "Infraestructura como código, pipelines de CI/CD, canary releases y observabilidad desde el primer despliegue. Coste por consulta y latencia visibles para todo el mundo.",
    out: ["IaC en tu nube o on-prem", "CI/CD y canary", "Dashboards de coste y calidad", "Plan de rollback probado"],
  },
  {
    label: "Operar",
    when: "Después",
    title: "Te lo dejamos funcionando",
    body: "Runbooks, formación y handover a tu equipo. Si lo prefieres, seguimos operando con SLAs y mejoramos el sistema con los datos que genera en producción.",
    out: ["Runbooks y documentación", "Formación al equipo", "SRE y guardias opcionales", "Mejora continua con datos"],
  },
];

const stats = [
  { value: 17, suffix: "", label: "proyectos con testimonio de cliente" },
  { value: 30, suffix: "+", label: "devs senior liderados en un único programa" },
  { value: 6, suffix: "", label: "meses de cero a producción en HBS" },
  { value: 7, suffix: "", label: "capas del stack, un único equipo" },
];

function Stats() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: "-15% 0px" });
  return (
    <div ref={ref} className="grid grid-cols-2 gap-x-6 gap-y-10 lg:grid-cols-4">
      {stats.map((s) => (
        <div key={s.label} className="border-t border-blanco/15 pt-7">
          <div className="font-display text-7xl font-extralight leading-none tracking-[-0.04em] text-lima md:text-8xl">
            <NumberFlow value={inView ? s.value : 0} suffix={s.suffix} />
          </div>
          <p className="mt-3 max-w-[240px] text-[15px] text-blanco/60">{s.label}</p>
        </div>
      ))}
    </div>
  );
}

export function Method() {
  return (
    <section id="metodo" className="bg-negro">
      <div className="mx-auto max-w-[1440px] px-4 py-28 md:px-16 md:py-36">
        <p className="font-mono text-xs uppercase tracking-[0.1em] text-lima">06 — Método</p>
        <h2 className="font-display mt-6 text-5xl font-extralight leading-[1.02] tracking-[-0.03em] md:text-7xl">
          Entramos. Construimos.
          <br />
          Nos quedamos lo justo.
        </h2>

        <div className="mt-14">
          <DirectionAwareTabs
            className="border border-blanco/10 bg-blanco/[0.06] p-1"
            tabs={steps.map((s, i) => ({
              id: i,
              label: s.label,
              content: (
                <div className="mt-8 grid gap-10 rounded-[28px] border border-blanco/8 bg-azul p-8 md:p-12 lg:grid-cols-[1.4fr_1fr]">
                  <div>
                    <p className="font-mono text-xs text-lima">{s.when}</p>
                    <h3 className="font-display mt-4 text-3xl tracking-[-0.02em] md:text-[2.5rem]">{s.title}</h3>
                    <p className="mt-5 max-w-[620px] text-[17px] font-light leading-relaxed text-blanco/72">{s.body}</p>
                  </div>
                  <ul className="flex flex-col gap-3">
                    {s.out.map((o) => (
                      <li
                        key={o}
                        className="flex items-center gap-3 rounded-xl border border-blanco/8 bg-blanco/[0.04] px-4 py-3 text-[15px] text-blanco/90"
                      >
                        <span className="font-mono text-lima">✓</span>
                        {o}
                      </li>
                    ))}
                  </ul>
                </div>
              ),
            }))}
          />
        </div>

        <div className="mt-24">
          <Stats />
        </div>
      </div>
    </section>
  );
}
