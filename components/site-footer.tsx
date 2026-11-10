export default function SiteFooter() {
  return (
    <footer className="mt-auto border-t border-mud bg-beige/40">
      <div className="flex flex-col gap-2 px-4 py-8 text-b3 text-ink/70 sm:flex-row sm:items-center sm:justify-between sm:px-6 font-sans">
        <p>© {new Date().getFullYear()} Barkada of Santa Clara University</p>
        <p>KAA — placeholder footer copy</p>
      </div>
    </footer>
  );
}
