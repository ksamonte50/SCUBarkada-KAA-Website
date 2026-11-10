"use client";

import { useEffect } from "react";

/*
 * Tree module host.
 *
 * Reproduces the required legacy DOM elements by fixed id so PyScript and
 * zoom.js can bind to them properly while matching the new Figma design.
 */

const PYSCRIPT_BASE = "https://pyscript.net/releases/2024.7.1";

/* Absolute paths: /tree has no trailing slash, so a relative "app.py" would
 * resolve to /app.py instead of /tree/app.py. Empty destination = basename
 * in the root of PyScript's virtual filesystem. */
const MPY_CONFIG = `{
  "files": {
    "/tree/app.py": "",
    "/tree/draw.py": "",
    "/tree/animation.py": "",
    "/tree/svgnodes.py": ""
  }
}`;

const RUNTIME_ATTR = "data-kaa-tree-runtime";

function tag(el: Element) {
  el.setAttribute(RUNTIME_ATTR, "");
  return el;
}

function loadStylesheet(href: string) {
  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.href = href;
  document.head.appendChild(tag(link));
}

function loadScript(opts: { src: string; type?: string }) {
  const script = document.createElement("script");
  script.src = opts.src;
  if (opts.type) script.type = opts.type;
  document.head.appendChild(tag(script));
}

function bootTreeRuntime() {
  if (document.querySelector(`script[${RUNTIME_ATTR}]`)) return;

  // 1. Config first — PyScript reads it when core.js evaluates.
  const config = document.createElement("mpy-config");
  config.textContent = MPY_CONFIG;
  document.body.appendChild(tag(config));

  const entry = document.createElement("script");
  entry.type = "mpy";
  entry.src = "/tree/treeclass.py";
  entry.async = true;
  document.body.appendChild(tag(entry));

  // 2. PyScript's own stylesheet, then the tree's.
  loadStylesheet(`${PYSCRIPT_BASE}/core.css`);
  loadStylesheet("/tree/tree.css");

  // 3. zoom.js before core.js, matching document order.
  loadScript({ src: "/tree/zoom.js" });
  loadScript({ src: `${PYSCRIPT_BASE}/core.js`, type: "module" });
}

export default function TreeModule() {
  useEffect(() => {
    bootTreeRuntime();

    // Keydown listener on search input to trigger tree creation on Enter
    const input = document.getElementById("tree_name") as HTMLInputElement | null;
    const testBtn = document.getElementById("testButton") as HTMLButtonElement | null;
    if (!input || !testBtn) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Enter") {
        e.preventDefault();
        testBtn.click();
      }
    };
    input.addEventListener("keydown", handleKeyDown);
    return () => input.removeEventListener("keydown", handleKeyDown);
  }, []);

  return (
    <div
      id="svg-container"
      className="relative w-full h-full bg-[#e5dfcc] rounded-xl overflow-hidden shadow-sm flex flex-col"
    >
      {/* ── Loading Screen ── */}
      <div
        id="load-screen"
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-20 font-['Cabinet_Grotesk',sans-serif] text-2xl font-medium text-[#1e2a1e] tracking-wide pointer-events-none"
      >
        Loading...
      </div>

      {/* ── Zoom Controls (Figma buttons top right) ── */}
      <div
        id="zoom-box-new"
        className="absolute top-5 right-5 z-10 flex items-center gap-2.5"
      >
        <button
          type="button"
          id="plus-zoom"
          className="size-10 bg-[#1e2a1e] text-white font-['Cabinet_Grotesk',sans-serif] text-xl font-medium flex items-center justify-center shadow-[0px_2px_8px_0px_rgba(0,0,0,0.15)] hover:bg-[#2e3e2e] transition-colors cursor-pointer"
          title="Zoom In"
        >
          +
        </button>
        <button
          type="button"
          id="minus-zoom"
          className="size-10 bg-[#1e2a1e] text-white font-['Cabinet_Grotesk',sans-serif] text-xl font-medium flex items-center justify-center shadow-[0px_2px_8px_0px_rgba(0,0,0,0.15)] hover:bg-[#2e3e2e] transition-colors cursor-pointer"
          title="Zoom Out"
        >
          -
        </button>
      </div>

      {/* ── Search & Help Controls (Figma bottom center) ── */}
      <div className="absolute bottom-6 left-1/2 -translate-x-1/2 z-10 flex items-center gap-3">
        {/* Search bar container */}
        <div id="autocomplete-container" className="relative w-[256px]">
          <div className="w-[256px] h-10 bg-white shadow-[0px_2px_8px_0px_rgba(0,0,0,0.15)] flex items-center px-2.5 gap-2.5">
            <img
              src="/icons/search.svg"
              alt=""
              width={18}
              height={18}
              className="size-[18px] shrink-0 opacity-60"
            />
            <input
              type="text"
              id="tree_name"
              placeholder="Search..."
              autoComplete="off"
              className="w-full h-full bg-transparent border-0 outline-none font-['Cabinet_Grotesk',sans-serif] text-base font-medium text-[#1e2a1e] placeholder:text-black/30"
            />
          </div>
        </div>

        {/* Hidden button triggered to build the tree */}
        <button type="button" id="testButton" style={{ display: "none" }}>
          Click!
        </button>

        {/* Help button */}
        <button
          type="button"
          id="helpButton"
          className="size-10 min-w-10 bg-[#1e2a1e] text-white font-['Cabinet_Grotesk',sans-serif] text-[19px] font-medium flex items-center justify-center shadow-[0px_2px_8px_0px_rgba(0,0,0,0.15)] hover:bg-[#2e3e2e] transition-colors cursor-pointer"
          title="Help"
        >
          ?
        </button>
      </div>

      {/* ── Help Box Modal ── */}
      <div
        id="help-box"
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-30 w-[90%] max-w-[480px] bg-white rounded-xl shadow-2xl p-6 border border-[#948e79]/30 font-['Cabinet_Grotesk',sans-serif]"
        style={{ display: "none" }}
      >
        <div className="flex items-center justify-between pb-3 border-b border-[#e5dfcc]">
          <h2 className="text-2xl font-bold text-[#1e2a1e]">How to Use</h2>
          <button
            type="button"
            id="closeButton"
            className="text-xl text-[#948e79] hover:text-[#1e2a1e] font-bold px-2 py-1 cursor-pointer transition-colors"
          >
            ✕
          </button>
        </div>

        <ol className="mt-4 space-y-2 text-sm text-[#1e2a1e]/90 list-decimal pl-5">
          <li>Type a name into the search bar and select or press Enter.</li>
          <li>Hover over any name to see how they connect to you.</li>
          <li>Click any person on the tree to rebuild the tree around them.</li>
        </ol>

        <h3 className="mt-5 text-base font-bold text-[#1e2a1e] border-t border-[#e5dfcc] pt-3">
          What Do All the Colors Mean?
        </h3>
        <div className="mt-3 space-y-2 text-sm">
          <div className="flex items-center gap-2.5">
            <span className="size-4 rounded-[4px] bg-[#1e2a1e] shrink-0" />
            <span className="text-[#1e2a1e]">
              <strong className="font-semibold">Dark Green:</strong> Selected tree root
            </span>
          </div>
          <div className="flex items-center gap-2.5">
            <span className="size-4 rounded-[4px] bg-[#3a523a] shrink-0" />
            <span className="text-[#1e2a1e]">
              <strong className="font-semibold">Forest Green:</strong> Direct relatives
            </span>
          </div>
          <div className="flex items-center gap-2.5">
            <span className="size-4 rounded-[4px] bg-[#a2591f] shrink-0" />
            <span className="text-[#1e2a1e]">
              <strong className="font-semibold">Rust Orange:</strong> Co-pickups
            </span>
          </div>
          <div className="flex items-center gap-2.5">
            <span className="size-4 rounded-[4px] bg-[#948e79] shrink-0" />
            <span className="text-[#1e2a1e]">
              <strong className="font-semibold">Mud Taupe:</strong> Appears elsewhere on tree
            </span>
          </div>
        </div>

        <button
          type="button"
          onClick={() => {
            const hb = document.getElementById("help-box");
            if (hb) hb.style.display = "none";
          }}
          className="mt-6 w-full py-2.5 bg-[#1e2a1e] hover:bg-[#2e3e2e] text-white font-medium rounded-lg transition-colors cursor-pointer"
        >
          Close
        </button>
      </div>

      {/* ── SVG Drawing Canvas ── */}
      <svg
        id="svg-drawing"
        className="w-full h-full bg-[#e5dfcc] cursor-grab active:cursor-grabbing block"
      >
        <defs id="defs">
          <filter id="shadow" width="125%" height="125%">
            <feDropShadow dx="0" dy="4" stdDeviation="2.5" />
          </filter>
          <filter id="line-shadow" width="125%" height="125%">
            <feDropShadow dx="2" dy="4" stdDeviation="2.5" />
          </filter>
        </defs>
      </svg>
    </div>
  );
}
