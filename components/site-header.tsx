"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function SiteHeader() {
  const pathname = usePathname();

  if (pathname === "/tree") {
    return null;
  }

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

  const isHomeActive = pathname === "/";
  const isAboutActive = pathname.startsWith("/about");
  const isTreeActive = pathname.startsWith("/tree");

  const leftNavItems = [
    { href: "/", label: "Home", isActive: isHomeActive },
    { href: "/about", label: "About", isActive: isAboutActive },
  ] as const;

  const treeHref = "/tree";
  const baseTreeClass =
    "flex items-center justify-center gap-[7px] px-[16px] py-[8px] font-sans text-b1 font-medium leading-normal whitespace-nowrap text-center text-white transition-all duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/70";
  const treeStateClass = isTreeActive
    ? "bg-green-dark drop-shadow-[0px_2px_4px_rgba(0,0,0,0.15)]"
    : "bg-orange hover:bg-green-dark hover:drop-shadow-[0px_2px_4px_rgba(0,0,0,0.15)]";
  const combinedTreeClass = `${baseTreeClass} ${treeStateClass}`;

  return (
    <header
      className={`${
        isHomeActive ? "absolute" : "sticky"
      } top-0 left-0 right-0 z-40 flex w-full justify-center px-4 pt-4 pb-2 pointer-events-none`}
    >
      <nav
        aria-label="Main"
        className="pointer-events-auto relative flex h-[64px] w-full max-w-[620px] items-center justify-between bg-[rgba(58,82,58,0.6)] backdrop-blur-md px-[20px] shadow-[0px_2px_8px_0px_rgba(0,0,0,0.15)]"
      >
        <div className="flex items-center gap-[16px] shrink-0">
          {leftNavItems.map((item) => {
            const baseClass =
              "flex items-center justify-center px-[16px] py-[8px] font-sans text-b1 font-medium leading-normal whitespace-nowrap text-center transition-all duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/70";
            const stateClass =
              item.isActive && !isHomeActive
                ? "bg-green-dark text-white drop-shadow-[0px_2px_4px_rgba(0,0,0,0.15)]"
                : item.isActive
                ? "text-white"
                : "text-beige hover:bg-green-dark hover:text-white hover:drop-shadow-[0px_2px_4px_rgba(0,0,0,0.15)]";
            const combinedClass = `${baseClass} ${stateClass}`;

            return hardNav(item.href) ? (
              <a key={item.href} href={item.href} className={combinedClass}>
                {item.label}
              </a>
            ) : (
              <Link key={item.href} href={item.href} className={combinedClass}>
                {item.label}
              </Link>
            );
          })}
        </div>

        {hardNav(treeHref) ? (
          <a href={treeHref} className={combinedTreeClass}>
            <span>Tree</span>
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
        ) : (
          <Link href={treeHref} className={combinedTreeClass}>
            <span>Tree</span>
            <div className="relative shrink-0 size-[20px]">
              <img
                src="/arrow-forward.svg"
                alt=""
                width={20}
                height={20}
                className="block size-full"
              />
            </div>
          </Link>
        )}
      </nav>
    </header>
  );
}
