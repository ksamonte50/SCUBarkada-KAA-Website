// svg-drawing is an svg
const container = document.getElementById("svg-container");
const drawing = document.getElementById("svg-drawing");
const VIEWBOX_OFFSET = 150
const ZOOM_BOX_MULTIPLIER = 0.25

// CHANGE THESE VALUES IF YOU CHANGE THE (container) SIZE
var defaultWidth = 700;
var defaultHeight = 400;

var drawingPosition = drawing.getBoundingClientRect(); // getBoundingClientRect() gives distance from edges of the window. 

var viewBox = {x: 0, y: 0, width: defaultWidth, height: defaultHeight};

var scale = 1;
// movement variables
var isPanning = false;
var startPoint = {x: 0, y: 0};
var endPoint = {x: 0, y: 0};
var currentTouchDistance = 0;

document.body.onload = function() {
	drawing.setAttribute('value', `${viewBox.x} ${viewBox.y} ${viewBox.width} ${viewBox.height}`)
	drawing.setAttribute('viewBox', `${viewBox.x} ${viewBox.y} ${viewBox.width} ${viewBox.height}`);
	checkSize()
}

// logic for help box
var helpButton = document.getElementById("helpButton");
var helpBox = document.getElementById("help-box");
var closeButton = document.getElementById("closeButton");
helpButton.onclick = () => {
	helpBox.style.display="block";
};

closeButton.onclick = () => {
	helpBox.style.display = "none";
};


// this function updates the position and size of the svg, since it can be resized and repositioned.
var checkSize = function() {
	defaultWidth = drawing.clientWidth;
	defaultHeight = drawing.clientHeight;
	
	scale = defaultWidth / viewBox.width;
	drawingPosition = drawing.getBoundingClientRect();
	// container.style.height = `${defaultHeight}px`
};

// Event listener for canvas switching event. Used to center the canvas over the new node.
document.getElementById("svg-drawing").addEventListener("setsvgcenter", ()=>{
	let data = document.getElementById("svg-drawing").getAttribute("value");
	console.log(`svg: ${Number(data)}`);

	checkSize()
	viewBox.width = defaultWidth
	viewBox.height = defaultHeight
	nodes = document.getElementsByClassName("main-root") // get the last node of the class list for most recent main-root
	mainRoot = nodes[nodes.length-1]
	viewBox.x = (-1 * defaultWidth / 2) + Number(data);
	viewBox.y = -1 * defaultHeight / 2;
	scale = 1;
	drawing.setAttribute('viewBox', `${viewBox.x} ${viewBox.y} ${viewBox.width} ${viewBox.height}`);
})

// ---------- scroll zoom in/out (wheel behavior) ----------
drawing.onwheel = function(e) {
	checkSize();
	e.preventDefault(); // prevents the scrolling behavior of mousewheel
	if(!isPanning) {
		let mouseX = e.clientX - drawingPosition.left;
		let mouseY = e.clientY - drawingPosition.top;

		let deltaW = viewBox.width * Math.sign(e.deltaY) * 0.05;
		let deltaH = viewBox.height * Math.sign(e.deltaY) * 0.05;
		let deltaX = deltaW * mouseX / defaultWidth;
		let deltaY = deltaH * mouseY / defaultHeight;

		viewBox = {
			x: viewBox.x + deltaX, 
			y: viewBox.y + deltaY, 
			width: viewBox.width - deltaW, 
			height: viewBox.height - deltaH
		};

		scale = defaultWidth / viewBox.width;

		drawing.setAttribute('viewBox', `${viewBox.x} ${viewBox.y} ${viewBox.width} ${viewBox.height}`);
	}
}

// ---------- scroll zoom in/out (zoom box) ----------
document.getElementById("plus-zoom").onclick = function(e) {
	e.preventDefault()
	checkSize();
	if(!isPanning) {
		let mouseX = (viewBox.width / 2) + drawingPosition.left;
		let mouseY = (viewBox.height / 2) + drawingPosition.top;

		let deltaW = viewBox.width * ZOOM_BOX_MULTIPLIER;
		let deltaH = viewBox.height * ZOOM_BOX_MULTIPLIER;
		let deltaX = deltaW * mouseX / defaultWidth;
		let deltaY = deltaH * mouseY / defaultHeight;

		viewBox = {
			x: viewBox.x + deltaX, 
			y: viewBox.y + deltaY, 
			width: viewBox.width - deltaW, 
			height: viewBox.height - deltaH
		};

		scale = defaultWidth / viewBox.width;

		drawing.setAttribute('viewBox', `${viewBox.x} ${viewBox.y} ${viewBox.width} ${viewBox.height}`);
	}
}

document.getElementById("minus-zoom").onclick = function(e) {
	e.preventDefault()
	checkSize();
	if(!isPanning) {
		let mouseX = (viewBox.width / 2) + drawingPosition.left;
		let mouseY = (viewBox.height / 2) + drawingPosition.top;

		let deltaW = viewBox.width * -2 * ZOOM_BOX_MULTIPLIER;
		let deltaH = viewBox.height * -2 * ZOOM_BOX_MULTIPLIER;
		let deltaX = deltaW * mouseX / defaultWidth;
		let deltaY = deltaH * mouseY / defaultHeight;

		viewBox = {
			x: viewBox.x + deltaX, 
			y: viewBox.y + deltaY, 
			width: viewBox.width - deltaW, 
			height: viewBox.height - deltaH
		};

		scale = defaultWidth / viewBox.width;

		drawing.setAttribute('viewBox', `${viewBox.x} ${viewBox.y} ${viewBox.width} ${viewBox.height}`);
	}
}

// ----------- moving the svg (mouse down/up/move/leave behavior) ------------
var mousedown = function(e) {
	checkSize();
	isPanning = true;
	startPoint = {x: e.clientX, y: e.clientY};	
}

var mousemove = function(e) {
	if (isPanning) {
		endPoint = {
			x: e.clientX, 
			y: e.clientY
		};
		let dx = (startPoint.x - endPoint.x) / scale;
		let dy = (startPoint.y - endPoint.y) / scale;
		let movedViewBox = {
			x: viewBox.x + dx,
			y: viewBox.y + dy,
			width: viewBox.width,
			height: viewBox.height
		}
		drawing.setAttribute('viewBox', `${movedViewBox.x} ${movedViewBox.y} ${movedViewBox.width} ${movedViewBox.height}`);
	}
}

var mouseup = function(e) {
	if(isPanning) {
		endPoint = {
			x: e.clientX, 
			y: e.clientY
		};
		let dx = (startPoint.x - endPoint.x) / scale;
		let dy = (startPoint.y - endPoint.y) / scale;
		viewBox.x += dx;
		viewBox.y += dy;
		drawing.setAttribute('viewBox', `${viewBox.x} ${viewBox.y} ${viewBox.width} ${viewBox.height}`);
		isPanning = false;
	}
}

var mouseleave = function(e) {
	if(isPanning) {
		endPoint = {
			x: e.clientX, 
			y: e.clientY
		};
		let dx = (startPoint.x - endPoint.x) / scale;
		let dy = (startPoint.y - endPoint.y) / scale;
		viewBox.x += dx;
		viewBox.y += dy;
		drawing.setAttribute('viewBox', `${viewBox.x} ${viewBox.y} ${viewBox.width} ${viewBox.height}`);
	}
	isPanning = false;
}

drawing.onmousedown = (e) => {
	e.preventDefault()
	mousedown(e)
}

drawing.onmousemove = (e) => {
	e.preventDefault()
	mousemove(e)
}

drawing.onmouseup = (e) => {
	e.preventDefault()
	mouseup(e)
}

drawing.onmouseleave = (e) => {
	e.preventDefault()
	mouseleave(e)
}

var currentTouch;
var currentMovedTouch;

drawing.ontouchstart = (e) => {
	currentTouch = e.touches[0]
	currentMovedTouch = e.changedTouches[0]
	e.stopPropagation()
	e.preventDefault()
	mousedown(e.touches[0]);
}

drawing.ontouchmove = (e) => {
	e.stopPropagation()
	e.preventDefault()
	currentMovedTouch = e.changedTouches[0]
	mousemove(currentMovedTouch)
}

drawing.ontouchend = (e) => {
	e.stopPropagation()
	e.preventDefault()
	mouseup(currentMovedTouch)
}

drawing.ontouchcancel = (e) => {
	e.stopPropagation()
	e.preventDefault()
	mouseleave(currentMovedTouch)
}