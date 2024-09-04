// svg-drawing is an svg
const container = document.getElementById("svg-container");
const drawing = document.getElementById("svg-drawing");

// CHANGE THESE VALUES IF YOU CHANGE THE (container) SIZE
var defaultWidth = 700;
var defaultHeight = 700;

var drawingPosition = drawing.getBoundingClientRect(); // getBoundingClientRect() gives distance from edges of the window. 

var viewBox = {x: 0, y: 0, width: defaultWidth, height: defaultHeight};

var scale = 1;
// movement variables
var isPanning = false;
var startPoint = {x: 0, y: 0};
var endPoint = {x: 0, y: 0};

document.body.onload = function() {
	drawing.setAttribute('viewBox', `${viewBox.x} ${viewBox.y} ${viewBox.width} ${viewBox.height}`);
}

// this function updates the position and size of the svg, since it can be resized and repositioned.
var checkSize = function() {
	defaultWidth = drawing.clientWidth;
	defaultHeight = drawing.clientHeight;
	
	scale = defaultWidth / viewBox.width;
	drawingPosition = drawing.getBoundingClientRect();
};

// ---------- scroll zoom in/out (wheel behavior) ----------
drawing.onwheel = function(e) {
	checkSize();
	e.preventDefault(); // prevents the scrolling behavior of mousewheel
	if(!isPanning) {
		let mouseX = e.x - drawingPosition.left;
		let mouseY = e.y - drawingPosition.top;

		let deltaW = viewBox.width * Math.sign(e.deltaY) * 0.07;
		let deltaH = viewBox.height * Math.sign(e.deltaY) * 0.07;
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

drawing.onmousedown = function(e) {
	checkSize();
	e.preventDefault();
	isPanning = true;
	startPoint = {x: e.x, y: e.y};
}

drawing.onmousemove = function(e) {
	if (isPanning) {
		e.preventDefault();
		endPoint = {
			x: e.x, 
			y: e.y
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

drawing.onmouseup = function(e) {
	e.preventDefault();
	if(isPanning) {
		endPoint = {
			x: e.x, 
			y: e.y
		};
		let dx = (startPoint.x - endPoint.x) / scale;
		let dy = (startPoint.y - endPoint.y) / scale;
		viewBox.x += dx;
		viewBox.y += dy;
		drawing.setAttribute('viewBox', `${viewBox.x} ${viewBox.y} ${viewBox.width} ${viewBox.height}`);
		isPanning = false;
	}
}

drawing.onmouseleave = function(e) {
	if(isPanning) {
		endPoint = {
			x: e.x, 
			y: e.y
		};
		let dx = (startPoint.x - endPoint.x) / scale;
		let dy = (startPoint.y - endPoint.y) / scale;
		viewBox.x += dx;
		viewBox.y += dy;
		drawing.setAttribute('viewBox', `${viewBox.x} ${viewBox.y} ${viewBox.width} ${viewBox.height}`);
	}
	isPanning = false;
}