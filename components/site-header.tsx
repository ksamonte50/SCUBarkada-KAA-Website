"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV = [
  { href: "/", label: "Home" },
  { href: "/about", label: "About" },
  { href: "/tree", label: "Tree" },
] as const;

export default function SiteHeader() {
  const pathname = usePathname();

  /*
   * The Tree page hosts a PyScript interpreter that mutates the document
   * directly and registers window-level listeners. A soft navigation away
   * from it would leave that runtime alive in the same document, so:
   *
   *   - leaving /tree  -> plain <a>, full load
   *   - going to /tree -> plain <a>, full load (fresh interpreter)
   *
   * Home <-> About stays client-side navigated as usual.
   */
  const hardNav = (href: string) => pathname === "/tree" || href === "/tree";

  return (
    <header className="sticky top-0 z-40 border-b border-border bg-bg/85 backdrop-blur-sm">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6">
        <Link
          href="/"
          className="flex items-center gap-3 font-semibold tracking-tight text-ink"
        >
          {/* Placeholder mark — swap public/logo.svg for the real asset */}
          <img
            src="/logo.svg"
            alt=""
            width={36}
            height={36}
            className="size-9 rounded-lg"
          />
          <span className="text-sm sm:text-base">
            Barkada of SCU
            <span className="block text-xs font-normal text-ink-muted">
              KAA
            </span>
          </span>
        </Link>

        <nav aria-label="Main">
          <ul className="flex items-center gap-1 sm:gap-2">
            {NAV.map((item) => {
              const className =
                "rounded-lg px-3 py-2 text-sm font-medium text-ink-muted transition-colors hover:bg-accent-soft hover:text-ink";

              return (
                <li key={item.href}>
                  {hardNav(item.href) ? (
                    <a href={item.href} className={className}>
                      {item.label}
                    </a>
                  ) : (
                    <Link href={item.href} className={className}>
                      {item.label}
                    </Link>
                  )}
                </li>
              );
            })}
          </ul>
        </nav>
      </div>
    </header>
  );
}
