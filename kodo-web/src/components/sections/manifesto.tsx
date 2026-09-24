import { ScrollChars } from "@/components/skiper/scroll-chars";

export function Manifesto() {
  return (
    <section aria-label="Manifiesto" className="bg-blanco text-negro">
      <ScrollChars text="Del píxel al prompt" accentFrom={13}>
        <p className="flex items-center gap-3 text-lg font-light md:text-2xl">
          <span className="font-display text-5xl font-extralight md:text-6xl">{"{"}</span>
          un solo equipo, todo el ciclo de vida
          <span className="font-display text-5xl font-extralight md:text-6xl">{"}"}</span>
        </p>
        <p className="max-w-[720px] text-center text-lg font-light leading-relaxed text-negro/75 md:text-xl">
          Kodo 360 no es una agencia de diseño ni una consultora de IA. Es el
          equipo que se queda desde el primer wireframe hasta el último token
          servido en producción.
        </p>
      </ScrollChars>
    </section>
  );
}
