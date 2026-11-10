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
        <p className="mb-4 text-sm font-semibold uppercase tracking-widest text-accent">
          {/* PLACEHOLDER */}
          Santa Clara University
        </p>

        <h1
          className="max-w-3xl font-semibold tracking-tight text-ink"
          style={{ fontSize: "var(--text-display)", lineHeight: 1.05 }}
        >
          {/* PLACEHOLDER */}
          Barkada of SCU&apos;s KAA
        </h1>

        <p className="mt-6 max-w-2xl text-lg leading-relaxed text-ink-muted">
          {/* PLACEHOLDER */}
          A short paragraph introducing the org goes here — who you are, what
          KAA stands for, and what the barkada is about.
        </p>

        <div className="mt-10 flex flex-wrap gap-3">
          {/* Plain <a>: /tree needs a full page load so PyScript boots fresh */}
          <a
            href="/tree"
            className="rounded-xl bg-accent px-6 py-3 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-accent-hover"
          >
            Explore the tree
          </a>
          <Link
            href="/about"
            className="rounded-xl border border-border bg-surface px-6 py-3 text-sm font-semibold text-ink transition-colors hover:border-accent hover:text-accent"
          >
            About us
          </Link>
        </div>
      </section>

      {/* ── Feature strip ───────────────────────────────────────────── */}
      <section className="border-t border-border bg-surface">
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
              className="border-b border-border px-4 py-10 sm:border-b-0 sm:border-r sm:px-6 sm:last:border-r-0"
            >
              <h2 className="text-base font-semibold text-ink">{card.title}</h2>
              <p className="mt-3 text-sm leading-relaxed text-ink-muted">
                {card.body}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Tree CTA ────────────────────────────────────────────────── */}
      <section className="px-4 py-20 text-center sm:px-6">
        <h2
          className="font-semibold tracking-tight text-ink"
          style={{ fontSize: "var(--text-heading)", lineHeight: 1.15 }}
        >
          {/* PLACEHOLDER */}
          See how everyone connects
        </h2>
        <p className="mx-auto mt-4 max-w-xl text-ink-muted">
          {/* PLACEHOLDER */}
          Search your name and follow the lines up and down the family tree.
        </p>
        <a
          href="/tree"
          className="mt-8 inline-block rounded-xl bg-accent px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-accent-hover"
        >
          Open the tree
        </a>
      </section>
    </>
  );
}
