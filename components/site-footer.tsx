"use client";

import { usePathname } from "next/navigation";

export default function SiteFooter() {
  const pathname = usePathname();

  // Hide footer on home hero and interactive tree page
  if (pathname === "/" || pathname === "/tree") {
    return null;
  }

  return (
    <footer className="mt-auto border-t border-mud bg-beige/40">
      <div className="flex flex-col gap-2 px-4 py-8 font-sans text-b3 text-ink/70 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <p>© {new Date().getFullYear()} Barkada of Santa Clara University</p>
        <p>KAA — placeholder footer copy</p>
      </div>
    </footer>
  );
}
