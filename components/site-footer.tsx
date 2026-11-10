"use client";

import { usePathname } from "next/navigation";

export default function SiteFooter() {
  const pathname = usePathname();

  if (pathname === "/tree") {
    return null;
  }

  return (
    <footer className="mt-auto border-t border-border">
      <div className="flex flex-col gap-2 px-4 py-8 text-sm text-ink-muted sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <p>© {new Date().getFullYear()} Barkada of Santa Clara University</p>
        <p>KAA — placeholder footer copy</p>
      </div>
    </footer>
  );
}
