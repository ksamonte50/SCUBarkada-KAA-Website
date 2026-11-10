import Link from "next/link";

/*
 * HOME — placeholder copy.
 *
 * Every string on this page is a stand-in. Replace the marked sections with
 * your own writing; the layout should hold up as-is.
 */

export default function HomePage() {
  return (
    <>
      {/* ── Hero ─────────────────────────────────────────────────────── */}
      <section className="px-4 pb-16 pt-16 sm:px-6 sm:pb-24 sm:pt-24">
        <p className="mb-4 text-note text-orange">
          {/* PLACEHOLDER */}
          Santa Clara University
        </p>

        <h1
          className="max-w-3xl font-display font-medium tracking-tight text-ink"
          style={{ fontSize: "var(--text-display)", lineHeight: 1.05 }}
        >
          {/* PLACEHOLDER */}
          Barkada of SCU&apos;s KAA
        </h1>

        <p className="mt-6 max-w-2xl text-b1 leading-relaxed text-ink/80 font-sans">
          {/* PLACEHOLDER */}
          A short paragraph introducing the org goes here — who you are, what
          KAA stands for, and what the barkada is about.
        </p>

        <div className="mt-10 flex flex-wrap gap-3">
          {/* Plain <a>: /tree needs a full page load so PyScript boots fresh */}
          <a
            href="/tree"
            className="flex items-center gap-[7px] bg-orange px-6 py-3 font-sans text-b2 font-medium text-white shadow-sm transition-all duration-150 hover:bg-green-dark"
          >
            <span>Explore the tree</span>
            <div className="relative shrink-0 size-[20px]">
              <img
                src="/arrow-forward.svg"
                alt=""
                width={20}
                height={20}
                className="block size-full"
              />
            </div>
          </a>
          <Link
            href="/about"
            className="border border-mud bg-transparent px-6 py-3 font-sans text-b2 font-medium text-ink transition-all duration-150 hover:bg-green-dark hover:text-white hover:border-green-dark"
          >
            About us
          </Link>
        </div>
      </section>

      {/* ── Feature strip ───────────────────────────────────────────── */}
      <section className="border-t border-mud bg-surface/40">
        <div className="grid overflow-hidden sm:grid-cols-3">
          {[
            {
              title: "Our story",
              body: "PLACEHOLDER — one or two sentences about the org's history and roots.",
            },
            {
              title: "The barkada",
              body: "PLACEHOLDER — what membership means, and what the community does together.",
            },
            {
              title: "Get involved",
              body: "PLACEHOLDER — how to reach out, pledge, or just come say hi.",
            },
          ].map((card) => (
            <div
              key={card.title}
              className="border-b border-mud px-4 py-10 sm:border-b-0 sm:border-r sm:px-6 sm:last:border-r-0"
            >
              <h2 className="text-h4 text-ink">{card.title}</h2>
              <p className="mt-3 text-b2 leading-relaxed text-ink/80">
                {card.body}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Tree CTA ────────────────────────────────────────────────── */}
      <section className="px-4 py-20 text-center sm:px-6">
        <h2
          className="font-display font-medium tracking-tight text-ink"
          style={{ fontSize: "var(--text-heading)", lineHeight: 1.15 }}
        >
          {/* PLACEHOLDER */}
          See how everyone connects
        </h2>
        <p className="mx-auto mt-4 max-w-xl text-b1 text-ink/80">
          {/* PLACEHOLDER */}
          Search your name and follow the lines up and down the family tree.
        </p>
        <a
          href="/tree"
          className="mt-8 inline-flex items-center gap-[7px] bg-orange px-6 py-3 font-sans text-b2 font-medium text-white transition-all duration-150 hover:bg-green-dark"
        >
          <span>Open the tree</span>
          <div className="relative shrink-0 size-[20px]">
            <img
              src="/arrow-forward.svg"
              alt=""
              width={20}
              height={20}
              className="block size-full"
            />
          </div>
        </a>
      </section>
    </>
  );
}
