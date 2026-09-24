"use client";

import { motion, useMotionValueEvent, useScroll } from "motion/react";
import { useState } from "react";

import { TextRoll } from "@/components/skiper/text-roll";
import { cn } from "@/lib/utils";

const links = [
  ["01", "Servicios", "#servicios"],
  ["02", "IA · FDE", "#ia"],
  ["03", "Proyectos", "#proyectos"],
  ["04", "Método", "#metodo"],
] as const;

export function Logo({ className }: { className?: string }) {
  return (
    <a href="#top" className={cn("flex items-center gap-2.5", className)}>
      <svg viewBox="0 0 26 26" className="size-6" aria-hidden>
        <circle
          cx="13"
          cy="13"
          r="10.5"
          fill="none"
          stroke="var(--color-lima)"
          strokeWidth="4"
          strokeDasharray="58 8"
          strokeLinecap="round"
          transform="rotate(-60 13 13)"
        />
      </svg>
      <span className="font-display text-2xl font-semibold tracking-tight">
        kodo
      </span>
      <span className="font-display -ml-1 text-2xl font-extralight text-lima">
        360
      </span>
    </a>
  );
}

export function Nav() {
  const { scrollY } = useScroll();
  const [scrolled, setScrolled] = useState(false);
  useMotionValueEvent(scrollY, "change", (v) => setScrolled(v > 40));

  return (
    <motion.header
      initial={{ y: -40, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
      className={cn(
        "fixed inset-x-0 top-0 z-50 transition-[background-color,backdrop-filter,border-color] duration-500",
        scrolled
          ? "border-b border-blanco/10 bg-negro/85 backdrop-blur-xl"
          : "border-b border-transparent",
      )}
    >
      <nav className="mx-auto flex max-w-[1440px] items-center justify-between px-4 py-5 md:px-16">
        <Logo />
        <ul className="hidden items-center gap-9 lg:flex">
          {links.map(([n, label, href]) => (
            <li key={href}>
              <a href={href} className="flex items-start gap-1.5">
                <span className="font-mono text-[10px] text-lima">{n}</span>
                <TextRoll className="text-[15px] text-blanco/85">
                  {label}
                </TextRoll>
              </a>
            </li>
          ))}
        </ul>
        <a
          href="#contacto"
          className="group flex items-center gap-2 rounded-full bg-lima px-5 py-2.5 text-[15px] text-negro transition-transform hover:scale-[1.03]"
        >
          ¿Hablamos?
          <span className="font-mono transition-transform group-hover:translate-x-0.5">
            →
          </span>
        </a>
      </nav>
    </motion.header>
  );
}
