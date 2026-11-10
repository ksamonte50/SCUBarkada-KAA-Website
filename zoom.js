// svg-drawing zoom & pan controller
const container = document.getElementById("svg-container");
const drawing = document.getElementById("svg-drawing");
const VIEWBOX_OFFSET = 150;
const ZOOM_BOX_MULTIPLIER = 0.25;

var defaultWidth = 700;
var defaultHeight = 400;

var drawingPosition = drawing
  ? drawing.getBoundingClientRect()
  : { left: 0, top: 0, width: defaultWidth, height: defaultHeight };

var viewBox = { x: -defaultWidth / 2, y: -defaultHeight / 2, width: defaultWidth, height: defaultHeight };
var scale = 1;
var isPanning = false;
var startPoint = { x: 0, y: 0 };
var startViewBox = { x: 0, y: 0, width: defaultWidth, height: defaultHeight };
var hasDragged = false;

function checkSize() {
  if (!drawing) return;
  const rect = drawing.getBoundingClientRect();
  defaultWidth = rect.width || drawing.clientWidth || 700;
  defaultHeight = rect.height || drawing.clientHeight || 400;
  scale = defaultWidth / (viewBox.width || defaultWidth);
  drawingPosition = rect;
}

function initDrawing() {
  if (drawing) {
    checkSize();
    viewBox.width = defaultWidth;
    viewBox.height = defaultHeight;
    viewBox.x = -defaultWidth / 2;
    viewBox.y = -defaultHeight / 2;
    drawing.setAttribute("value", `${viewBox.x} ${viewBox.y} ${viewBox.width} ${viewBox.height}`);
    drawing.setAttribute("viewBox", `${viewBox.x} ${viewBox.y} ${viewBox.width} ${viewBox.height}`);
  }
}

if (document.readyState === "complete" || document.readyState === "interactive") {
  initDrawing();
} else {
  window.addEventListener("load", initDrawing);
}

// Help box logic
var helpButton = document.getElementById("helpButton");
var helpBox = document.getElementById("help-box");
var closeButton = document.getElementById("closeButton");
if (helpButton) {
  helpButton.onclick = () => {
    if (helpBox) helpBox.style.display = "block";
  };
}
if (closeButton) {
  closeButton.onclick = () => {
    if (helpBox) helpBox.style.display = "none";
  };
}

if (drawing) {
  drawing.addEventListener("setsvgcenter", () => {
    let data = drawing.getAttribute("value");
    checkSize();
    viewBox.width = defaultWidth;
    viewBox.height = defaultHeight;
    viewBox.x = -defaultWidth / 2 + (Number(data) || 0);
    viewBox.y = -defaultHeight / 2;
    scale = 1;
    drawing.setAttribute("viewBox", `${viewBox.x} ${viewBox.y} ${viewBox.width} ${viewBox.height}`);
  });
}

function zoomBy(factor, clientX, clientY) {
  if (!drawing) return;
  checkSize();
  const targetW = viewBox.width * factor;
  const targetH = viewBox.height * factor;
  if (targetW < 80 || targetW > 50000) return;

  const rect = drawing.getBoundingClientRect();
  const screenX = clientX !== undefined ? clientX - rect.left : rect.width / 2;
  const screenY = clientY !== undefined ? clientY - rect.top : rect.height / 2;

  const fracX = Math.max(0, Math.min(1, screenX / (rect.width || defaultWidth)));
  const fracY = Math.max(0, Math.min(1, screenY / (rect.height || defaultHeight)));

  const anchorX = viewBox.x + fracX * viewBox.width;
  const anchorY = viewBox.y + fracY * viewBox.height;

  viewBox = {
    x: anchorX - fracX * targetW,
    y: anchorY - fracY * targetH,
    width: targetW,
    height: targetH,
  };
  scale = defaultWidth / viewBox.width;
  drawing.setAttribute("viewBox", `${viewBox.x} ${viewBox.y} ${viewBox.width} ${viewBox.height}`);
}

// Zoom controls (+ / -)
var plusBtn = document.getElementById("plus-zoom");
if (plusBtn) {
  plusBtn.onclick = function (e) {
    e.preventDefault();
    zoomBy(0.8);
  };
}

var minusBtn = document.getElementById("minus-zoom");
if (minusBtn) {
  minusBtn.onclick = function (e) {
    e.preventDefault();
    zoomBy(1.25);
  };
}

// Mouse wheel zoom
if (drawing) {
  drawing.addEventListener(
    "wheel",
    function (e) {
      e.preventDefault();
      const factor = e.deltaY < 0 ? 0.9 : 1.1;
      zoomBy(factor, e.clientX, e.clientY);
    },
    { passive: false }
  );
}

// Mouse drag pan
if (drawing) {
  drawing.addEventListener("mousedown", function (e) {
    if (e.button !== 0) return;
    checkSize();
    isPanning = true;
    hasDragged = false;
    startPoint = { x: e.clientX, y: e.clientY };
    startViewBox = { ...viewBox };
  });

  window.addEventListener("mousemove", function (e) {
    if (!isPanning || !drawing) return;
    const dxScreen = e.clientX - startPoint.x;
    const dyScreen = e.clientY - startPoint.y;
    if (Math.hypot(dxScreen, dyScreen) > 4) {
      hasDragged = true;
    }
    const rect = drawing.getBoundingClientRect();
    const unitsPerPxX = startViewBox.width / (rect.width || defaultWidth);
    const unitsPerPxY = startViewBox.height / (rect.height || defaultHeight);
    viewBox = {
      x: startViewBox.x - dxScreen * unitsPerPxX,
      y: startViewBox.y - dyScreen * unitsPerPxY,
      width: startViewBox.width,
      height: startViewBox.height,
    };
    drawing.setAttribute("viewBox", `${viewBox.x} ${viewBox.y} ${viewBox.width} ${viewBox.height}`);
  });

  window.addEventListener("mouseup", function () {
    isPanning = false;
  });

  drawing.addEventListener(
    "click",
    function (e) {
      if (hasDragged) {
        e.stopPropagation();
        e.preventDefault();
        hasDragged = false;
      }
    },
    true
  );
}
