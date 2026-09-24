import { Nav } from "@/components/nav";
import { Contact } from "@/components/sections/contact";
import { Fde } from "@/components/sections/fde";
import { Footer } from "@/components/sections/footer";
import { Hero } from "@/components/sections/hero";
import { Manifesto } from "@/components/sections/manifesto";
import { Method } from "@/components/sections/method";
import { Projects } from "@/components/sections/projects";
import { Stack } from "@/components/sections/stack";

export default function Home() {
  return (
    <>
      <Nav />
      <main>
        <Hero />
        <Manifesto />
        <Stack />
        <Fde />
        <Projects />
        <Method />
        <Contact />
      </main>
      <Footer />
    </>
  );
}
