import type { Metadata } from "next";
import { Raleway, Roboto, Roboto_Mono } from "next/font/google";

import { SmoothScroll } from "@/components/smooth-scroll";

import "./globals.css";

const raleway = Raleway({
  variable: "--font-raleway",
  subsets: ["latin"],
  weight: ["200", "300", "400", "600"],
});

const roboto = Roboto({
  variable: "--font-roboto",
  subsets: ["latin"],
  weight: ["300", "400", "500"],
});

const robotoMono = Roboto_Mono({
  variable: "--font-roboto-mono",
  subsets: ["latin"],
  weight: ["400", "500"],
});

export const metadata: Metadata = {
  title: "Kodo 360 — Del píxel al modelo",
  description:
    "Diseño, desarrollo, arquitectura de software, infraestructura, DevOps e IA aplicada. Forward deployed engineers especializados en RAG, agentes y guardrails.",
  openGraph: {
    title: "Kodo 360 — Del píxel al modelo",
    description:
      "Un solo equipo para todo el ciclo: del primer wireframe al último token servido en producción.",
    siteName: "Kodo 360",
    locale: "es_ES",
    type: "website",
  },
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="es"
      className={`${raleway.variable} ${roboto.variable} ${robotoMono.variable} antialiased`}
    >
      <body>
        <SmoothScroll>{children}</SmoothScroll>
      </body>
    </html>
  );
}
