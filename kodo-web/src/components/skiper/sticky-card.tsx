"use client";

/**
 * Adaptado de Skiper UI — skiper16 "Card stack scroll" (https://skiper-ui.com).
 * Autor: @gurvinder-singh02. Uso libre con atribución.
 */
import { motion, useTransform, type MotionValue } from "motion/react";
import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

export function StickyCard({
  i,
  progress,
  range,
  targetScale,
  className,
  children,
}: {
  i: number;
  progress: MotionValue<number>;
  range: [number, number];
  targetScale: number;
  className?: string;
  children: ReactNode;
}) {
  const scale = useTransform(progress, range, [1, targetScale]);
  const brightness = useTransform(progress, range, [1, 0.7]);
  const filter = useTransform(brightness, (b) => `brightness(${b})`);

  return (
    <div className="sticky top-0 flex h-screen items-center justify-center">
      <motion.div
        style={{ scale, filter, top: `calc(-5vh + ${i * 28}px)` }}
        className={cn(
          "relative flex h-[440px] w-full max-w-[720px] origin-top flex-col overflow-hidden rounded-[2rem]",
          className,
        )}
      >
        {children}
      </motion.div>
    </div>
  );
}
