import type { Metadata } from "next";
import Image from "next/image";

export const metadata: Metadata = {
  title: "KAAnect | Barkada of SCU",
  description:
    "Barkada presents KAAnect — Santa Clara University's KAA family tree.",
};

export default function HomePage() {
  return (
    <section className="relative flex min-h-screen w-full flex-col items-center justify-center overflow-hidden bg-black px-4 py-24 select-none sm:px-6">
      {/* Background leaves with black base */}
      <div className="pointer-events-none absolute inset-0 z-0">
        <Image
          src="/hero-leaves.png"
          alt=""
          fill
          priority
          sizes="100vw"
          className="object-cover object-center opacity-55"
        />
      </div>

      {/* Hero content */}
      <div className="relative z-10 flex flex-col items-center text-center">
        <p className="font-display text-[24px] font-medium leading-normal text-white sm:text-[32px]">
          Barkada presents
        </p>

        <h1 className="mt-[20px] font-display text-[48px] font-medium leading-none tracking-normal text-white sm:mt-[31px] sm:text-[64px]">
          KAAnect
        </h1>

        <a
          href="/tree"
          className="mt-[24px] inline-flex items-center justify-center gap-[7px] bg-orange px-[16px] py-[8px] font-sans text-b1 font-medium leading-normal text-white shadow-sm transition-all duration-150 hover:bg-green-dark focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/70 sm:mt-[31px]"
        >
          <span>Tree</span>
          <div className="relative size-[20px] shrink-0">
            <img
              src="/arrow-forward.svg"
              alt=""
              width={20}
              height={20}
              className="block size-full"
            />
          </div>
        </a>
      </div>
    </section>
  );
}
