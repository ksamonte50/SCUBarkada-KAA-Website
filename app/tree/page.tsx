import type { Metadata } from "next";
import TreeModule from "@/components/tree/tree-module";

export const metadata: Metadata = {
  title: "Tree",
  description:
    "Explore the Barkada of SCU KAA big/little family tree.",
};

export default function TreePage() {
  return (
    <div className="relative flex flex-col h-screen w-screen overflow-hidden bg-[#948e79] font-['Cabinet_Grotesk',sans-serif]">
      {/* ── Top Floating Nav Bar v3 (Matches Figma node 133:374) ── */}
      <header className="pt-4 px-4 shrink-0 flex justify-center z-20">
        <nav
          aria-label="Main"
          className="w-full max-w-[512px] h-[64px] bg-[#3a523a] shadow-[0px_2px_4px_rgba(0,0,0,0.15)] flex items-center justify-between px-4 py-3"
        >
          <div className="flex items-center gap-4">
            <a
              href="/"
              className="px-4 py-2 font-['Cabinet_Grotesk',sans-serif] text-[19px] font-medium text-[#e5dfcc] hover:text-white transition-colors"
            >
              Home
            </a>
            <a
              href="/about"
              className="px-4 py-2 font-['Cabinet_Grotesk',sans-serif] text-[19px] font-medium text-[#e5dfcc] hover:text-white transition-colors"
            >
              About
            </a>
          </div>
    <div className="w-full px-4 py-8 sm:px-6">
      <div className="mb-6 max-w-2xl">
        <h1
          className="font-display font-medium tracking-tight text-ink text-h2"
        >
          The family tree
        </h1>
        <p className="mt-3 text-b1 text-ink/80 font-sans">
          Search for a name, then hover over anyone to see how you&apos;re
          connected. Click a name to rebuild the tree around them.
        </p>
      </div>

          <div className="bg-[#a2591f] flex items-center gap-[7px] px-4 py-2 font-['Cabinet_Grotesk',sans-serif] text-[19px] font-medium text-white shadow-sm select-none">
            <span>Tree</span>
            <img
              src="/icons/arrow-forward.svg"
              alt=""
              width={20}
              height={20}
              className="size-5 shrink-0"
            />
          </div>
        </nav>
      </header>

      {/* ── Main Tree Container (Matches Figma node 272:31) ── */}
      <main className="flex-1 w-full p-4 sm:p-7 pt-3 pb-6 overflow-hidden flex flex-col">
        <TreeModule />
      </main>
    </div>
  );
}
