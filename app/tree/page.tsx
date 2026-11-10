import type { Metadata } from "next";
import TreeModule from "@/components/tree/tree-module";

export const metadata: Metadata = {
  title: "Tree",
  description:
    "Search a name and explore the Barkada of SCU KAA big/little family tree.",
};

/*
 * The tree itself is driven by unmodified legacy Python/JS running under
 * PyScript — see components/tree/tree-module.tsx.
 *
 * Kept deliberately free of state so React never re-renders the legacy
 * markup underneath PyScript (which mutates those same nodes directly).
 */
export default function TreePage() {
  return (
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

      <TreeModule />
    </div>
  );
}
