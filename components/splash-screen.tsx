"use client";

import { useEffect, useState } from "react";
import Image from "next/image";

export default function SplashScreen() {
  const [shouldRender, setShouldRender] = useState(false);

  useEffect(() => {
    // Only show on first visit in this browser session
    try {
      if (sessionStorage.getItem("kaa_splash_seen")) {
        return;
      }
      sessionStorage.setItem("kaa_splash_seen", "true");
    } catch {
      // Storage blocked or restricted
    }

    setShouldRender(true);
  }, []);

  if (!shouldRender) return null;

  return (
    <div
      className="splash-overlay fixed inset-0 z-[9999] flex items-center justify-center bg-[#e5dfcc] select-none"
      onAnimationEnd={() => setShouldRender(false)}
      aria-hidden="true"
    >
      <div className="splash-content flex flex-col items-center">
        <div className="relative size-36 sm:size-48 md:size-56 drop-shadow-md">
          <Image
            src="/barkada-logo.png"
            alt="Barkada Logo"
            fill
            priority
            className="object-contain"
          />
        </div>
      </div>
    </div>
  );
}
