"use client";

/**
 * Adaptado de Skiper UI — skiper19 "SVG follow scroll" (https://skiper-ui.com).
 * Autor: @gurvinder-singh02. Uso libre con atribución.
 */
import { motion, useTransform, type MotionValue } from "motion/react";

export function LinePath({
  progress,
  className,
}: {
  progress: MotionValue<number>;
  className?: string;
}) {
  const pathLength = useTransform(progress, [0, 0.9], [0.05, 1]);

  return (
    <svg
      viewBox="0 0 700 1800"
      fill="none"
      preserveAspectRatio="none"
      className={className}
      aria-hidden
    >
      <motion.path
        d="M120 0 C 120 180 520 160 540 360 C 560 560 120 520 140 760 C 160 1000 600 920 580 1180 C 560 1420 160 1360 180 1560 C 190 1680 360 1760 520 1800"
        stroke="var(--color-lima)"
        strokeWidth="14"
        strokeLinecap="round"
        vectorEffect="non-scaling-stroke"
        style={{ pathLength }}
      />
    </svg>
  );
}
