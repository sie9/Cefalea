"use client";

import { motion, useInView } from "motion/react";
import { useEffect, useRef, useState } from "react";

import {
  TerminalAnimationCommandBar,
  TerminalAnimationContent,
  TerminalAnimationOutput,
  TerminalAnimationRoot,
  TerminalAnimationTabList,
  TerminalAnimationTabTrigger,
  TerminalAnimationTrailingPrompt,
  TerminalAnimationWindow,
  type TabContent,
} from "@/components/cult/terminal-animation";
import { cn } from "@/lib/utils";

const dim = "text-blanco/45";
const ok = "text-verde";
const live = "text-lima";

const tabs: TabContent[] = [
  {
    label: "discovery",
    command: "kodo fde init --client=acme --semanas=6",
    lines: [
      { text: "", delay: 80 },
      { text: "  entrando en el equipo de acme…", color: dim, delay: 300 },
      { text: "  entrevistas ······· 22 personas · 5 áreas", color: dim, delay: 220 },
      { text: "  fuentes ··········· sharepoint · confluence · erp · tickets", color: dim, delay: 220 },
      { text: "✓ 14 procesos mapeados · 3 candidatos a IA", color: ok, delay: 400 },
      { text: "✓ caso #1: soporte L1 — 38 % del volumen, ROI estimado 4,1x", color: ok, delay: 300 },
    ],
  },
  {
    label: "rag",
    command: "kodo rag build --src=sharepoint,confluence,erp",
    lines: [
      { text: "", delay: 80 },
      { text: "  chunking ·········· 48.210 documentos (semántico)", color: dim, delay: 260 },
      { text: "  embeddings ········ pgvector + bm25 híbrido", color: dim, delay: 260 },
      { text: "  reranker ·········· cross-encoder multilingüe", color: dim, delay: 260 },
      { text: "  permisos ·········· ACL heredadas por documento", color: dim, delay: 260 },
      { text: "✓ recall@10 = 0,94 · mrr = 0,81", color: ok, delay: 400 },
    ],
  },
  {
    label: "guardrails",
    command: "kodo guardrails apply --policy=pii,jailbreak,grounding",
    lines: [
      { text: "", delay: 80 },
      { text: "  entrada ··········· pii redaction · prompt injection", color: dim, delay: 260 },
      { text: "  salida ············ grounding obligatorio · citas", color: dim, delay: 260 },
      { text: "  negocio ··········· 12 políticas propias del cliente", color: dim, delay: 260 },
      { text: "✓ 0 fugas de PII en 5.000 ataques sintéticos", color: ok, delay: 400 },
      { text: "✓ 99,2 % de respuestas con cita verificable", color: ok, delay: 300 },
    ],
  },
  {
    label: "evals",
    command: "kodo evals run --suite=negocio --n=1200",
    lines: [
      { text: "", delay: 80 },
      { text: "  dataset ··········· 1.200 casos reales anonimizados", color: dim, delay: 260 },
      { text: "  jueces ············ humano + llm-as-judge calibrado", color: dim, delay: 260 },
      { text: "✓ exactitud 91 % · alucinación 0,6 %", color: ok, delay: 400 },
      { text: "✓ p95 820 ms · coste por 1k consultas 0,43 €", color: ok, delay: 300 },
    ],
  },
  {
    label: "ship",
    command: "kodo ship --env=prod --canary=10%",
    lines: [
      { text: "", delay: 80 },
      { text: "  canary 10 % ······· sin regresiones en 48 h", color: dim, delay: 300 },
      { text: "  rollout 100 % ····· trazas en OpenTelemetry", color: dim, delay: 300 },
      { text: "● en producción. handover y runbooks entregados.", color: live, delay: 500 },
    ],
  },
];

const caps = [
  ["RAG", "Recuperación híbrida, reranking y citas verificables sobre tus fuentes reales, respetando permisos."],
  ["Guardrails", "PII, jailbreaks, grounding y políticas de negocio aplicadas en cada entrada y cada respuesta."],
  ["Agentes", "Flujos con herramientas, aprobación humana en los puntos críticos y trazabilidad de cada paso."],
  ["Evals", "Suites propias por caso de uso. Si no se mide, no pasa a producción."],
  ["LLMOps", "Observabilidad, coste por consulta, versionado de prompts y cambio de modelo sin miedo."],
  ["On-prem & soberanía", "Modelos abiertos en tu nube o tu CPD cuando los datos no pueden salir."],
] as const;

const models = ["Claude", "GPT", "Gemini", "Llama", "Mistral", "pgvector", "LangGraph", "vLLM", "OpenTelemetry", "Qdrant"];

function tabDuration(t: TabContent) {
  return 300 + t.command.length * 45 + 250 + t.lines.reduce((a, l) => a + (l.delay ?? 100), 0) + 2600;
}

function Terminal() {
  const [active, setActive] = useState(0);
  const [auto, setAuto] = useState(true);

  useEffect(() => {
    if (!auto) return;
    const id = setTimeout(() => setActive((a) => (a + 1) % tabs.length), tabDuration(tabs[active]));
    return () => clearTimeout(id);
  }, [active, auto]);

  return (
    <TerminalAnimationRoot
      tabs={tabs}
      activeTab={active}
      onActiveTabChange={(i) => {
        setAuto(false);
        setActive(i);
      }}
      hideCursorOnComplete={false}
      className="relative"
    >
      <TerminalAnimationWindow
        animateOnVisible={false}
        minHeight="27rem"
        backgroundColor="var(--color-negro)"
        className="rounded-[18px] border border-blanco/12 shadow-[0_30px_80px_-20px_rgba(0,0,0,0.55)]"
      >
        <div className="flex items-center gap-2 border-b border-blanco/8 bg-blanco/[0.04] px-4 py-3">
          <span className="size-[11px] rounded-full bg-blanco/25" />
          <span className="size-[11px] rounded-full bg-blanco/25" />
          <span className="size-[11px] rounded-full bg-blanco/25" />
          <span className="ml-3 font-mono text-xs text-blanco/50">kodo@fde — acme-prod</span>
        </div>
        <TerminalAnimationTabList className="flex gap-1 overflow-x-auto border-b border-blanco/8 px-3 py-2">
          {tabs.map((t, i) => (
            <TerminalAnimationTabTrigger
              key={t.label}
              index={i}
              className="shrink-0 rounded-md px-3 py-1 font-mono text-[12px] text-blanco/50 transition-colors hover:text-blanco data-[state=active]:bg-lima data-[state=active]:text-negro"
            >
              {String(i + 1).padStart(2, "0")} {t.label}
            </TerminalAnimationTabTrigger>
          ))}
        </TerminalAnimationTabList>
        <TerminalAnimationContent className="px-5 py-5 font-mono text-[13px] leading-[1.75] sm:px-7 md:text-sm">
          <div className="flex gap-3">
            <span className="text-lima">$</span>
            <TerminalAnimationCommandBar
              className="text-blanco"
              cursor={<span className="ml-0.5 inline-block h-[17px] w-[8px] translate-y-[3px] bg-lima" />}
            />
          </div>
          <TerminalAnimationOutput
            renderLine={(line, _i, visible) =>
              visible ? (
                <motion.div
                  initial={{ opacity: 0, x: -6 }}
                  animate={{ opacity: 1, x: 0 }}
                  className={cn("whitespace-pre-wrap", line.color ?? "text-blanco/80")}
                >
                  {line.text || " "}
                </motion.div>
              ) : null
            }
          />
          <TerminalAnimationTrailingPrompt className="mt-1 flex gap-3">
            <span className="text-lima">$</span>
            <span className="animate-caret-blink inline-block h-[17px] w-[8px] translate-y-[3px] bg-lima" />
          </TerminalAnimationTrailingPrompt>
        </TerminalAnimationContent>
      </TerminalAnimationWindow>
    </TerminalAnimationRoot>
  );
}

function CapCard({ title, desc, i }: { title: string; desc: string; i: number }) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-10% 0px" }}
      transition={{ duration: 0.7, delay: (i % 2) * 0.08 + Math.floor(i / 2) * 0.06, ease: [0.16, 1, 0.3, 1] }}
      onPointerMove={(e) => {
        const r = e.currentTarget.getBoundingClientRect();
        e.currentTarget.style.setProperty("--mx", `${e.clientX - r.left}px`);
        e.currentTarget.style.setProperty("--my", `${e.clientY - r.top}px`);
      }}
      className="group relative overflow-hidden rounded-[18px] border border-blanco/10 bg-azul/55 p-6 shadow-[inset_0_1px_0_rgba(255,255,255,0.06)]"
    >
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 opacity-0 transition-opacity duration-300 group-hover:opacity-100"
        style={{
          background:
            "radial-gradient(260px circle at var(--mx) var(--my), rgba(172,231,50,0.16), transparent 70%)",
        }}
      />
      {/* línea de "escaneo": el guardrail revisando la tarjeta */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-x-0 top-0 h-px -translate-y-2 bg-gradient-to-r from-transparent via-lima to-transparent opacity-0 transition-all duration-[900ms] group-hover:translate-y-[180px] group-hover:opacity-100"
      />
      <h3 className="font-display relative flex items-center gap-2.5 text-xl font-semibold">
        <span className="size-2 rounded-[2px] bg-lima" />
        {title}
      </h3>
      <p className="relative mt-3 text-sm font-light leading-relaxed text-blanco/70">{desc}</p>
    </motion.article>
  );
}

export function Fde() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: "-20% 0px" });

  return (
    <section id="ia" className="bg-teal">
      <div className="mx-auto max-w-[1440px] px-4 py-28 md:px-16 md:py-36">
        <div className="flex flex-col justify-between gap-10 lg:flex-row lg:items-end">
          <div>
            <p className="font-mono text-xs uppercase tracking-[0.1em] text-lima">04 — Forward deployed engineering</p>
            <h2 className="font-display mt-6 text-5xl font-extralight leading-[1.02] tracking-[-0.03em] md:text-[5rem]">
              La IA no se entrega
              <br />
              en una demo.
            </h2>
          </div>
          <p className="max-w-[440px] text-lg font-light leading-relaxed text-blanco/80">
            Nos incrustamos en tu equipo, con tus datos y tus restricciones, hasta
            que el sistema está en producción, medido y gobernado. Después te lo
            dejamos funcionando y documentado.
          </p>
        </div>

        <div className="mt-16 grid grid-cols-1 gap-8 lg:grid-cols-[1.15fr_1fr]">
          <div ref={ref} className="min-h-[27rem] min-w-0">
            {inView && (
              <motion.div
                initial={{ opacity: 0, y: 60 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 1, ease: [0.16, 1, 0.3, 1] }}
              >
                <Terminal />
              </motion.div>
            )}
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            {caps.map(([t, d], i) => (
              <CapCard key={t} title={t} desc={d} i={i} />
            ))}
          </div>
        </div>

        <div className="mt-16 flex items-center gap-8 overflow-hidden border-t border-blanco/15 pt-7">
          <span className="shrink-0 font-mono text-[11px] uppercase tracking-[0.08em] text-lima">
            Agnósticos de modelo →
          </span>
          <div className="relative flex-1 overflow-hidden [mask-image:linear-gradient(to_right,transparent,black_8%,black_92%,transparent)]">
            <div className="flex w-max animate-marquee gap-12">
              {[...models, ...models].map((m, i) => (
                <span key={i} className="font-display text-xl text-blanco/55">
                  {m}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
