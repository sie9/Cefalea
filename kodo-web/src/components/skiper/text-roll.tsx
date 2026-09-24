"use client";

/**
 * Adaptado de Skiper UI — skiper58 "Text roll navigation" (https://skiper-ui.com).
 * Autor: @gurvinder-singh02. Uso libre con atribución.
 */
import { motion } from "motion/react";

import { cn } from "@/lib/utils";

const STAGGER = 0.035;

export function TextRoll({
  children,
  className,
  center = false,
}: {
  children: string;
  className?: string;
  center?: boolean;
}) {
  const letters = children.split("");
  const delayFor = (i: number) =>
    center
      ? STAGGER * Math.abs(i - (letters.length - 1) / 2)
      : STAGGER * i;

  return (
    <motion.span
      initial="initial"
      whileHover="hovered"
      className={cn("relative block overflow-hidden leading-[0.95]", className)}
      aria-label={children}
    >
      <span aria-hidden className="block">
        {letters.map((l, i) => (
          <motion.span
            key={i}
            variants={{ initial: { y: 0 }, hovered: { y: "-100%" } }}
            transition={{ ease: "easeInOut", delay: delayFor(i) }}
            className="inline-block whitespace-pre"
          >
            {l}
          </motion.span>
        ))}
      </span>
      <span aria-hidden className="absolute inset-0 block">
        {letters.map((l, i) => (
          <motion.span
            key={i}
            variants={{ initial: { y: "100%" }, hovered: { y: 0 } }}
            transition={{ ease: "easeInOut", delay: delayFor(i) }}
            className="inline-block whitespace-pre text-lima"
          >
            {l}
          </motion.span>
        ))}
      </span>
    </motion.span>
  );
}
