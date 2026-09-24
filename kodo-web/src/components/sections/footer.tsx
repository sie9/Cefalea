"use client";

import { motion, useScroll, useTransform } from "motion/react";
import { useRef } from "react";

import { Logo } from "@/components/nav";
import { CssLink } from "@/components/skiper/css-link";

const cols = [
  ["Estudio", [["Servicios", "#servicios"], ["IA · FDE", "#ia"], ["Proyectos", "#proyectos"], ["Método", "#metodo"]]],
  ["Legal", [["Aviso legal", "#"], ["Privacidad", "#"], ["Cookies", "#"], ["Condiciones generales", "#"]]],
  ["Social", [["LinkedIn", "https://www.linkedin.com/company/kodo-360"], ["hola@kodo-360.com", "mailto:hola@kodo-360.com"]]],
] as const;

export function Footer() {
  const ref = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start end", "end end"] });
  const y = useTransform(scrollYProgress, [0, 1], ["45%", "0%"]);
  const rotateX = useTransform(scrollYProgress, [0, 1], [55, 0]);

  return (
    <footer ref={ref} className="overflow-hidden bg-azul">
      <div className="mx-auto max-w-[1440px] px-4 pt-20 md:px-16">
        <div className="flex flex-col justify-between gap-12 md:flex-row">
          <div className="max-w-[360px]">
            <Logo />
            <p className="mt-4 text-[15px] font-light leading-relaxed text-blanco/60">
              Estudio de ingeniería con base en Canarias. Diseño, desarrollo,
              arquitectura, infraestructura, DevOps e IA aplicada.
            </p>
          </div>
          <div className="grid grid-cols-2 gap-10 sm:grid-cols-3 md:gap-20">
            {cols.map(([h, items]) => (
              <div key={h}>
                <p className="font-mono text-[11px] uppercase tracking-[0.1em] text-lima">{h}</p>
                <ul className="mt-4 flex flex-col gap-3">
                  {items.map(([label, href]) => (
                    <li key={label}>
                      <CssLink href={href} className="text-[15px] text-blanco/75 hover:text-blanco">
                        {label}
                      </CssLink>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
        <div className="mt-14 flex flex-col justify-between gap-2 border-t border-blanco/12 pt-6 font-mono text-[11px] text-blanco/45 sm:flex-row">
          <span>© {new Date().getFullYear()} Kodo 360 · Las Palmas de Gran Canaria</span>
          <span>
            Animaciones con <a className="underline" href="https://skiper-ui.com">Skiper UI</a> &{" "}
            <a className="underline" href="https://www.cult-ui.com">Cult UI</a>
          </span>
        </div>
      </div>
      <div className="mt-6" style={{ perspective: "900px" }}>
        <motion.p
          aria-hidden
          style={{ y, rotateX, transformOrigin: "bottom" }}
          className="font-display select-none text-center text-[25vw] font-semibold leading-[0.78] tracking-[-0.06em] text-lima"
        >
          kodo360
        </motion.p>
      </div>
    </footer>
  );
}
