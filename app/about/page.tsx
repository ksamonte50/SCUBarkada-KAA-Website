import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About",
  description: "About Barkada of SCU's KAA — coming soon.",
};

/*
 * ABOUT — under construction.
 *
 * Deliberately minimal for now. When the real page lands, replace the
 * <section> body below; the header/footer come from the root layout.
 */
export default function AboutPage() {
  return (
    <section className="px-4 py-24 sm:px-6">
      <p className="mb-4 text-note text-orange">
        Coming soon
      </p>

      <h1
        className="font-display font-medium tracking-tight text-ink text-h2"
      >
        This page is under construction
      </h1>

      <p className="mt-5 max-w-lg text-b1 leading-relaxed text-ink/80 font-sans">
        {/* PLACEHOLDER — drop the real About copy in here when it's ready. */}
        We&apos;re putting together our story, our values, and how to get
        involved. Check back soon.
      </p>

      <div
        aria-hidden="true"
        className="mt-12 h-px w-40 bg-mud"
      />
    </section>
  );
}
