import type { Metadata } from "next";
import TreeModule from "@/components/tree/tree-module";

export const metadata: Metadata = {
  title: "Tree | Barkada KAAnect",
  description:
    "Explore the Barkada of SCU KAA big/little family tree.",
};

export default function TreePage() {
  return (
    <div
      className="relative flex flex-col h-screen h-[100dvh] w-full overflow-hidden bg-[#948e79] font-['Cabinet_Grotesk',sans-serif]"
      style={{ height: "100dvh" }}
    >
      {/* ── Main Tree Container (Sits below the fixed 64px header + top padding) ── */}
      <div
        className="flex-1 w-full p-4 sm:p-6 md:p-7 pb-6 sm:pb-6 md:pb-7 overflow-hidden flex flex-col"
        style={{ paddingTop: "100px" }}
      >
        <TreeModule />
      </div>
    </div>
  );
}
