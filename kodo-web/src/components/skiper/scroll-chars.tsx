"use client";

/**
 * Adaptado de Skiper UI — skiper31 "Text scroll animation" (https://skiper-ui.com).
 * Autor: @gurvinder-singh02. Uso libre con atribución.
 */
import { motion, useScroll, useTransform, type MotionValue } from "motion/react";
import { useRef } from "react";

import { cn } from "@/lib/utils";

function Character({
  char,
  index,
  centerIndex,
  progress,
  className,
}: {
  char: string;
  index: number;
  centerIndex: number;
  progress: MotionValue<number>;
  className?: string;
}) {
  const d = index - centerIndex;
  const x = useTransform(progress, [0, 0.5], [d * 50, 0]);
  const rotateX = useTransform(progress, [0, 0.5], [d * 50, 0]);
  const y = useTransform(progress, [0, 0.5], [Math.abs(d) * 12, 0]);

  return (
    <motion.span
      className={cn("inline-block", char === " " && "w-[0.3em]", className)}
      style={{ x, rotateX, y }}
    >
      {char}
    </motion.span>
  );
}

export function ScrollChars({
  text,
  accentFrom,
  className,
  children,
}: {
  text: string;
  /** Índice desde el que las letras se pintan con el color de acento */
  accentFrom?: number;
  className?: string;
  children?: React.ReactNode;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({ target: ref });
  const chars = text.split("");
  const centerIndex = Math.floor(chars.length / 2);

  return (
    <div
      ref={ref}
      className={cn(
        "relative flex h-[210vh] items-start justify-center",
        className,
      )}
    >
      <div className="sticky top-0 flex h-screen w-full flex-col items-center justify-center gap-10 overflow-hidden px-4">
        <h2
          aria-label={text}
          className="font-display w-full text-center text-[12vw] font-light uppercase leading-none tracking-tight md:text-[7.4vw]"
          style={{ perspective: "500px" }}
        >
          {chars.map((c, i) => (
            <Character
              key={i}
              char={c}
              index={i}
              centerIndex={centerIndex}
              progress={scrollYProgress}
              className={
                accentFrom !== undefined && i >= accentFrom
                  ? "font-semibold text-teal"
                  : undefined
              }
            />
          ))}
        </h2>
        {children}
      </div>
    </div>
  );
}
