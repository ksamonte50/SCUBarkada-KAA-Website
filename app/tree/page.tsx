import type { Metadata } from "next";
import TreeModule from "@/components/tree/tree-module";

export const metadata: Metadata = {
  title: "Tree",
  description:
    "Explore the Barkada of SCU KAA big/little family tree.",
};

export default function TreePage() {
  return (
    <div className="relative flex flex-col h-screen w-full overflow-hidden bg-[#948e79] font-['Cabinet_Grotesk',sans-serif]">
      {/* ── Main Tree Container (Matches Figma node 272:31) ── */}
      <div className="flex-1 w-full p-4 sm:p-7 pt-[88px] sm:pt-[92px] pb-6 overflow-hidden flex flex-col">
        <TreeModule />
      </div>
    </div>
  );
}
