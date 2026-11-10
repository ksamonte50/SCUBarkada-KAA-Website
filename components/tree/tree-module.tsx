"use client";

import { useEffect, useRef, useState, useCallback } from "react";

/*
 * Tree module host.
 *
 * Reproduces the required legacy DOM elements by fixed id so PyScript
 * can bind to them properly while matching the new Figma design.
 * Zoom, pan, and centering are managed natively to guarantee reliable
 * behavior across React renders, strict mode, and responsive resizes.
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

  // 3. PyScript runtime core
  loadScript({ src: `${PYSCRIPT_BASE}/core.js`, type: "module" });
}

interface ViewBox {
  x: number;
  y: number;
  width: number;
  height: number;
}

export default function TreeModule() {
  const svgRef = useRef<SVGSVGElement | null>(null);
  const [isHelpOpen, setIsHelpOpen] = useState(false);

  const viewBoxRef = useRef<ViewBox>({ x: -400, y: -300, width: 800, height: 600 });
  const isPanningRef = useRef(false);
  const startPointerRef = useRef({ x: 0, y: 0 });
  const startViewBoxRef = useRef<ViewBox>({ x: -400, y: -300, width: 800, height: 600 });
  const hasDraggedRef = useRef(false);

  const touchDistRef = useRef(0);
  const touchMidRef = useRef({ x: 0, y: 0 });

  const applyViewBox = useCallback(() => {
    const svg = svgRef.current;
    if (!svg) return;
    const vb = viewBoxRef.current;
    svg.setAttribute("viewBox", `${vb.x} ${vb.y} ${vb.width} ${vb.height}`);
    svg.setAttribute("value", `${vb.x} ${vb.y} ${vb.width} ${vb.height}`);
  }, []);

  const zoomAtPoint = useCallback(
    (factor: number, clientX?: number, clientY?: number) => {
      const svg = svgRef.current;
      if (!svg) return;
      const rect = svg.getBoundingClientRect();
      if (!rect.width || !rect.height) return;

      const cur = viewBoxRef.current;
      const MIN_WIDTH = 80;
      const MAX_WIDTH = 50000;
      const targetWidth = cur.width * factor;
      if (targetWidth < MIN_WIDTH || targetWidth > MAX_WIDTH) return;
      const targetHeight = cur.height * factor;

      const screenX = clientX !== undefined ? clientX - rect.left : rect.width / 2;
      const screenY = clientY !== undefined ? clientY - rect.top : rect.height / 2;

      const fracX = Math.max(0, Math.min(1, screenX / rect.width));
      const fracY = Math.max(0, Math.min(1, screenY / rect.height));

      const anchorX = cur.x + fracX * cur.width;
      const anchorY = cur.y + fracY * cur.height;

      viewBoxRef.current = {
        x: anchorX - fracX * targetWidth,
        y: anchorY - fracY * targetHeight,
        width: targetWidth,
        height: targetHeight,
      };
      applyViewBox();
    },
    [applyViewBox]
  );

  const handleZoomIn = useCallback(
    (e?: React.MouseEvent | MouseEvent) => {
      e?.preventDefault();
      zoomAtPoint(0.8);
    },
    [zoomAtPoint]
  );

  const handleZoomOut = useCallback(
    (e?: React.MouseEvent | MouseEvent) => {
      e?.preventDefault();
      zoomAtPoint(1.25);
    },
    [zoomAtPoint]
  );

  useEffect(() => {
    bootTreeRuntime();

    const svg = svgRef.current || (document.getElementById("svg-drawing") as SVGSVGElement | null);
    if (!svg) return;

    // Initialize viewBox to match current canvas size, centered at (0, 0)
    const rect = svg.getBoundingClientRect();
    const w = rect.width || 800;
    const h = rect.height || 600;
    viewBoxRef.current = {
      x: -w / 2,
      y: -h / 2,
      width: w,
      height: h,
    };
    applyViewBox();

    // ── PyScript tree centering event listener ──
    const handleSetSvgCenter = () => {
      const r = svg.getBoundingClientRect();
      const width = r.width || viewBoxRef.current.width || 800;
      const height = r.height || viewBoxRef.current.height || 600;
      const rawVal = svg.getAttribute("value");
      const rootX = Number(rawVal) || 0;

      viewBoxRef.current = {
        x: -width / 2 + rootX,
        y: -height / 2,
        width,
        height,
      };
      applyViewBox();
    };
    svg.addEventListener("setsvgcenter", handleSetSvgCenter);

    // ── Mouse wheel zoom centered under cursor ──
    const handleWheel = (e: WheelEvent) => {
      e.preventDefault();
      const factor = e.deltaY < 0 ? 0.9 : 1.1;
      zoomAtPoint(factor, e.clientX, e.clientY);
    };
    svg.addEventListener("wheel", handleWheel, { passive: false });

    // ── Mouse drag pan ──
    const handleMouseDown = (e: MouseEvent) => {
      if (e.button !== 0) return;
      isPanningRef.current = true;
      hasDraggedRef.current = false;
      startPointerRef.current = { x: e.clientX, y: e.clientY };
      startViewBoxRef.current = { ...viewBoxRef.current };
    };
    svg.addEventListener("mousedown", handleMouseDown);

    const handleMouseMove = (e: MouseEvent) => {
      if (!isPanningRef.current) return;
      const r = svg.getBoundingClientRect();
      if (!r.width || !r.height) return;

      const dxScreen = e.clientX - startPointerRef.current.x;
      const dyScreen = e.clientY - startPointerRef.current.y;

      if (Math.hypot(dxScreen, dyScreen) > 4) {
        hasDraggedRef.current = true;
      }

      const startVb = startViewBoxRef.current;
      const unitsPerPxX = startVb.width / r.width;
      const unitsPerPxY = startVb.height / r.height;

      viewBoxRef.current = {
        x: startVb.x - dxScreen * unitsPerPxX,
        y: startVb.y - dyScreen * unitsPerPxY,
        width: startVb.width,
        height: startVb.height,
      };
      applyViewBox();
    };
    window.addEventListener("mousemove", handleMouseMove);

    const handleMouseUp = () => {
      isPanningRef.current = false;
    };
    window.addEventListener("mouseup", handleMouseUp);

    // Suppress node click event if user was dragging/panning
    const handleClickCapture = (e: MouseEvent) => {
      if (hasDraggedRef.current) {
        e.stopPropagation();
        e.preventDefault();
        hasDraggedRef.current = false;
      }
    };
    svg.addEventListener("click", handleClickCapture, true);

    // ── Touch pan & pinch-to-zoom ──
    const handleTouchStart = (e: TouchEvent) => {
      if (e.touches.length === 1) {
        isPanningRef.current = true;
        hasDraggedRef.current = false;
        startPointerRef.current = { x: e.touches[0].clientX, y: e.touches[0].clientY };
        startViewBoxRef.current = { ...viewBoxRef.current };
      } else if (e.touches.length === 2) {
        isPanningRef.current = false;
        const t1 = e.touches[0];
        const t2 = e.touches[1];
        touchDistRef.current = Math.hypot(t2.clientX - t1.clientX, t2.clientY - t1.clientY);
        touchMidRef.current = {
          x: (t1.clientX + t2.clientX) / 2,
          y: (t1.clientY + t2.clientY) / 2,
        };
        startViewBoxRef.current = { ...viewBoxRef.current };
      }
    };
    svg.addEventListener("touchstart", handleTouchStart, { passive: false });

    const handleTouchMove = (e: TouchEvent) => {
      const r = svg.getBoundingClientRect();
      if (!r.width || !r.height) return;

      if (e.touches.length === 1 && isPanningRef.current) {
        e.preventDefault();
        const dxScreen = e.touches[0].clientX - startPointerRef.current.x;
        const dyScreen = e.touches[0].clientY - startPointerRef.current.y;

        if (Math.hypot(dxScreen, dyScreen) > 4) {
          hasDraggedRef.current = true;
        }

        const startVb = startViewBoxRef.current;
        const unitsPerPxX = startVb.width / r.width;
        const unitsPerPxY = startVb.height / r.height;

        viewBoxRef.current = {
          x: startVb.x - dxScreen * unitsPerPxX,
          y: startVb.y - dyScreen * unitsPerPxY,
          width: startVb.width,
          height: startVb.height,
        };
        applyViewBox();
      } else if (e.touches.length === 2 && touchDistRef.current > 0) {
        e.preventDefault();
        const t1 = e.touches[0];
        const t2 = e.touches[1];
        const newDist = Math.hypot(t2.clientX - t1.clientX, t2.clientY - t1.clientY);
        if (newDist < 10) return;
        const scaleRatio = touchDistRef.current / newDist;

        const startVb = startViewBoxRef.current;
        const newWidth = startVb.width * scaleRatio;
        const newHeight = startVb.height * scaleRatio;

        const mid = touchMidRef.current;
        const fracX = (mid.x - r.left) / r.width;
        const fracY = (mid.y - r.top) / r.height;

        const anchorX = startVb.x + fracX * startVb.width;
        const anchorY = startVb.y + fracY * startVb.height;

        viewBoxRef.current = {
          x: anchorX - fracX * newWidth,
          y: anchorY - fracY * newHeight,
          width: newWidth,
          height: newHeight,
        };
        applyViewBox();
      }
    };
    svg.addEventListener("touchmove", handleTouchMove, { passive: false });

    const handleTouchEnd = (e: TouchEvent) => {
      if (e.touches.length === 0) {
        isPanningRef.current = false;
        touchDistRef.current = 0;
      } else if (e.touches.length === 1) {
        isPanningRef.current = true;
        touchDistRef.current = 0;
        startPointerRef.current = { x: e.touches[0].clientX, y: e.touches[0].clientY };
        startViewBoxRef.current = { ...viewBoxRef.current };
      }
    };
    svg.addEventListener("touchend", handleTouchEnd);
    svg.addEventListener("touchcancel", handleTouchEnd);

    // ── Window resize: preserve aspect ratio smoothly ──
    const handleResize = () => {
      const r = svg.getBoundingClientRect();
      if (!r.width || !r.height) return;
      const cur = viewBoxRef.current;
      const newHeight = cur.width * (r.height / r.width);
      const diffH = newHeight - cur.height;
      viewBoxRef.current = {
        ...cur,
        y: cur.y - diffH / 2,
        height: newHeight,
      };
      applyViewBox();
    };
    window.addEventListener("resize", handleResize);

    // ── Search Enter keydown listener ──
    const input = document.getElementById("tree_name") as HTMLInputElement | null;
    const testBtn = document.getElementById("testButton") as HTMLButtonElement | null;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Enter") {
        e.preventDefault();
        testBtn?.click();
      }
    };
    if (input) {
      input.addEventListener("keydown", handleKeyDown);
    }

    return () => {
      svg.removeEventListener("setsvgcenter", handleSetSvgCenter);
      svg.removeEventListener("wheel", handleWheel);
      svg.removeEventListener("mousedown", handleMouseDown);
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
      svg.removeEventListener("click", handleClickCapture, true);
      svg.removeEventListener("touchstart", handleTouchStart);
      svg.removeEventListener("touchmove", handleTouchMove);
      svg.removeEventListener("touchend", handleTouchEnd);
      svg.removeEventListener("touchcancel", handleTouchEnd);
      window.removeEventListener("resize", handleResize);
      if (input) {
        input.removeEventListener("keydown", handleKeyDown);
      }
    };
  }, [applyViewBox, zoomAtPoint]);

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
          onClick={handleZoomIn}
          className="size-10 bg-[#1e2a1e] text-white font-['Cabinet_Grotesk',sans-serif] text-xl font-medium flex items-center justify-center shadow-[0px_2px_8px_0px_rgba(0,0,0,0.15)] hover:bg-[#2e3e2e] active:scale-95 transition-all cursor-pointer select-none"
          title="Zoom In"
        >
          +
        </button>
        <button
          type="button"
          id="minus-zoom"
          onClick={handleZoomOut}
          className="size-10 bg-[#1e2a1e] text-white font-['Cabinet_Grotesk',sans-serif] text-xl font-medium flex items-center justify-center shadow-[0px_2px_8px_0px_rgba(0,0,0,0.15)] hover:bg-[#2e3e2e] active:scale-95 transition-all cursor-pointer select-none"
          title="Zoom Out"
        >
          -
        </button>
      </div>

      {/* ── Search & Help Controls (Figma bottom center) ── */}
      <div className="absolute bottom-6 left-1/2 -translate-x-1/2 z-10 flex items-center gap-3">
        {/* Search bar container */}
        <div id="autocomplete-container" className="relative w-[256px] h-10 !pb-0 flex items-center">
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

        {/* Submit button to build the tree */}
        <button
          type="button"
          id="testButton"
          className="size-10 min-w-10 bg-[#1e2a1e] text-white flex items-center justify-center shadow-[0px_2px_8px_0px_rgba(0,0,0,0.15)] hover:bg-[#2e3e2e] active:scale-95 transition-all cursor-pointer"
          title="Search tree"
          aria-label="Build tree"
        >
          <img
            src="/arrow-forward.svg"
            alt=""
            width={20}
            height={20}
            className="size-5 shrink-0 block"
          />
        </button>

        {/* Help button */}
        <button
          type="button"
          id="helpButton"
          onClick={() => setIsHelpOpen((prev) => !prev)}
          className="size-10 min-w-10 bg-[#1e2a1e] text-white font-['Cabinet_Grotesk',sans-serif] text-[19px] font-medium flex items-center justify-center shadow-[0px_2px_8px_0px_rgba(0,0,0,0.15)] hover:bg-[#2e3e2e] active:scale-95 transition-all cursor-pointer"
          title="Help"
        >
          ?
        </button>
      </div>

      {/* ── Help Box Modal ── */}
      <div
        id="help-box"
        className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-30 w-[90%] max-w-[480px] bg-white rounded-xl shadow-2xl p-6 border border-[#948e79]/30 font-['Cabinet_Grotesk',sans-serif] ${
          isHelpOpen ? "block" : "hidden"
        }`}
        style={{ display: isHelpOpen ? "block" : "none" }}
      >
        <div className="flex items-center justify-between pb-3 border-b border-[#e5dfcc]">
          <h2 className="text-2xl font-bold text-[#1e2a1e]">How to Use</h2>
          <button
            type="button"
            id="closeButton"
            onClick={() => setIsHelpOpen(false)}
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
          onClick={() => setIsHelpOpen(false)}
          className="mt-6 w-full py-2.5 bg-[#1e2a1e] hover:bg-[#2e3e2e] text-white font-medium rounded-lg transition-colors cursor-pointer"
        >
          Close
        </button>
      </div>

      {/* ── SVG Drawing Canvas ── */}
      <svg
        ref={svgRef}
        id="svg-drawing"
        className="w-full h-full bg-[#e5dfcc] cursor-grab active:cursor-grabbing block touch-none select-none"
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
