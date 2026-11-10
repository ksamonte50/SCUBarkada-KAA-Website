"use client";

import { useEffect } from "react";

/*
 * Tree module host.
 *
 * The Python/JS/CSS that draws the tree is legacy code and must not be
 * modified. It reaches into the DOM by fixed id (see index.html in the repo
 * root), so this component reproduces that markup byte-for-byte and then
 * loads the runtime around it.
 *
 * Everything is injected imperatively in useEffect, in the same order the
 * original page used:
 *
 *   1. <mpy-config> + <script type="mpy">   (inert until PyScript boots)
 *   2. zoom.js                              (classic, ran during parse)
 *   3. pyscript core.js                     (module, deferred to the end)
 *
 * Injecting after mount guarantees the mpy elements already exist before
 * core.js evaluates. The guard stops React Strict Mode's double effect from
 * booting PyScript twice — note we deliberately never remove these on
 * unmount: removing the tags cannot un-evaluate core.js, and re-adding it
 * on a later mount would start a second interpreter.
 *
 * Navigating to/from /tree always uses a full page load (see site-header),
 * so the whole PyScript document is torn down on the way out.
 */

const PYSCRIPT_BASE = "https://pyscript.net/releases/2024.7.1";

/* Absolute paths: /tree has no trailing slash, so a relative "app.py" would
 * resolve to /app.py instead of /tree/app.py. Empty destination = basename
 * in the root of PyScript's virtual filesystem, exactly as before. */
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

  // 3. zoom.js before core.js, matching the original document order.
  loadScript({ src: "/tree/zoom.js" });
  loadScript({ src: `${PYSCRIPT_BASE}/core.js`, type: "module" });
}

export default function TreeModule() {
  useEffect(() => {
    bootTreeRuntime();
  }, []);

  return (
    <>
      {/* ── Controls ──────────────────────────────────────────────── */}
      <div className="flex flex-wrap items-center gap-3">
        <div id="autocomplete-container">
          <input
            type="text"
            id="tree_name"
            placeholder="Type a name here..."
            autoComplete="off"
          />
        </div>
        <button type="button" id="testButton" style={{ display: "none" }}>
          Click!
        </button>
        <button type="button" id="helpButton">
          Help!
        </button>
      </div>

      {/* ── Help box (hidden by default; Help!/Close toggle it) ───── */}
      <div id="help-box">
        <h1>How to Use</h1>
        <ol>
          <li>Type in your name.</li>
          <li>Click on &quot;Go!&quot; button.</li>
          <li>Hover over names to see how they are connected to you!</li>
          <li>Click on other names to see their tree!</li>
        </ol>
        <h3>What Do all the Colors Mean?</h3>
        <p>Purple = person who&apos;s tree has been built.</p>
        <p>Orange = people directly related to you.</p>
        <p>Light Blue = people who co-picked up into your tree.</p>
        <p>
          Red = Person who is already somewhere else on the tree. Hovering over
          them will show you where their counterpart is!
        </p>
        <button type="button" id="closeButton">
          Close
        </button>
      </div>

      {/* ── Canvas ────────────────────────────────────────────────── */}
      <div id="svg-container">
        <div id="load-screen">Loading...</div>
        <div id="zoom-box">
          <button type="button" className="zoom-button" id="plus-zoom">
            +
          </button>
          <button type="button" className="zoom-button" id="minus-zoom">
            -
          </button>
        </div>
        <svg id="svg-drawing">
          <defs id="defs">
            <filter id="shadow" width="125" height="125">
              <feDropShadow dx="0" dy="4" stdDeviation="2.5" />
            </filter>
            <filter id="line-shadow" width="125" height="125">
              <feDropShadow dx="2" dy="4" stdDeviation="2.5" />
            </filter>
          </defs>
        </svg>
      </div>
    </>
  );
}
