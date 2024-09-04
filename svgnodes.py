# This has the building blocks for svg content using the DOM

# Constants
NODE_WIDTH = 75
NODE_HEIGHT = 50

from draw import x_increments, y_increments, GHOST_LINE_OPACITY
from pyscript import document

# Creates an HTML node to place onto the svg element
# 	Parameters: 
# 		name {String} - innerHTML placed in the content 
#		color {HEX Color} - color of the node. could be hex or normal name
# 	Returns a "node", which is stored as [box, holder]
def make_node(name, color, opacity=1.0):
	# creates background holder 
	newElement = document.createElementNS('http://www.w3.org/2000/svg', 'rect')
	newElement.setAttribute('fill', f"{color}")
	newElement.setAttribute('rx', "20")
	newElement.setAttribute('ry', "20")
	newElement.setAttribute('opacity', f"{opacity}")
	newElement.setAttribute('width',f"{NODE_WIDTH}px")
	newElement.setAttribute('height',f"{NODE_HEIGHT}px")

	# create div holder
	holder = document.createElementNS('http://www.w3.org/2000/svg', 'foreignObject')
	holder.setAttribute('width', f"{NODE_WIDTH}px")
	holder.setAttribute('height', f"{NODE_HEIGHT}px")
	
	# create text content
	newTextContent = document.createElement('DIV')
	newTextContent.innerHTML = name
	newTextContent.setAttribute("style", f" \
		display: table-cell; \
		vertical-align: middle; \
		font-size: 11px; \
	")

	# create text holder
	newTextContainer = document.createElement('DIV')
	newTextContainer.setAttribute("style", f"\
		display: table; \
		width: {NODE_WIDTH}px; \
		height: {NODE_HEIGHT}px; \
		text-align: center; \
	")

	# append text to content and content to div holder
	newTextContainer.appendChild(newTextContent)
	holder.appendChild(newTextContainer)
	# nodes are lists of [rectangle, text_content]
	append_node([newElement, holder])
	return [newElement, holder]

# Adds node to the HTML svg element
# 	Parameters:
#		node {HTML element list} - node to append to webpage.
def append_node(node):
	document.getElementById('svg-drawing').appendChild(node[0])
	document.getElementById('svg-drawing').appendChild(node[1])

# Set x and y values of the HTML element in the svg canvas
#	Parameters:
#		node {HTML element list} - node to be updated
#		x {Number}
#		y {Number}
def set_node_position(node, x, y):
	node[0].setAttribute("x", f"{x - (NODE_WIDTH / 2)}")
	node[0].setAttribute("y", f"{y - (NODE_HEIGHT / 2)}")
	node[1].setAttribute("x", f"{x - (NODE_WIDTH / 2)}")
	node[1].setAttribute("y", f"{y - (NODE_HEIGHT / 2)}")

# Update an HTML node based on its x and y position in the hash map / dictionary
#	Parameters:
#		tree {Hash Map / Dictionary} - holds information about every person
#		person {String} - name of person to update.
#	This function is to be used in replacement of set_node_position if x and y is already stored.
def update_node_position(tree, person):
	if(tree[person]["visited"]):
		node = tree[person]["my_node"]
		set_node_position(node, tree[person]["x"], tree[person]["y"])

# Removes Nodes From SVG
def removeNodes():
	drawing = document.getElementById("svg-drawing")
	while(drawing.firstChild):
		drawing.removeChild(drawing.lastChild)
	addFilters()


# Adds this HTML to the SVG after all nodes are removed:
# <defs>
# 	<filter id="shadow" width="125" height="125">
# 		<feDropShadow dx="0" dy="4" stdDeviation="2.5"/>
# 	</filter>
# 	<filter id="line-shadow" width="125" height="125">
# 		<feDropShadow dx="1" dy="0" stdDeviation="2.5"/>
# 		<feGaussianBlur in="SourceGraphic" stdDeviation="0.9" />
# 	</filter>
# </defs>
def addFilters():
	defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs')
	nodeFilter = document.createElementNS('http://www.w3.org/2000/svg', 'filter')
	nodeFilter.setAttribute("id", "shadow")
	nodeFilter.setAttribute("width", "125")
	nodeFilter.setAttribute("height", "125")
	nodeShadow = document.createElementNS('http://www.w3.org/2000/svg', 'feDropShadow')
	nodeShadow.setAttribute("dx", "0")
	nodeShadow.setAttribute("dy", "4")
	nodeShadow.setAttribute("stdDeviation", "2.5")
	nodeFilter.appendChild(nodeShadow)

	lineFilter = document.createElementNS('http://www.w3.org/2000/svg', 'filter')
	lineFilter.setAttribute("id", "line-shadow")
	lineFilter.setAttribute("width", "125")
	lineFilter.setAttribute("height", "125")
	lineShadow = document.createElementNS('http://www.w3.org/2000/svg', 'feDropShadow')
	lineShadow.setAttribute("dx", "1")
	lineShadow.setAttribute("dy", "0")
	lineShadow.setAttribute("stdDeviation", "2.5")
	lineBlur = document.createElementNS('http://www.w3.org/2000/svg', 'feGaussianBlur')
	lineBlur.setAttribute("in", "SourceGraphic")
	lineBlur.setAttribute("stdDeviation", "0.9")

	lineFilter.appendChild(lineShadow)
	lineFilter.appendChild(lineBlur)

	defs.appendChild(nodeFilter)
	defs.appendChild(lineFilter)

	document.getElementById("svg-drawing").appendChild(defs)



# draw_full_tree(test2, "Elliot Bernardo")
# draw_full_tree(test, "Christian Chow")

# main_helper(test, "big 1")
# draw_lines(6)
# draw_tree_down(test, "big 1")

# draw_tree_down(test, "Kyle Samonte")

def draw_line_between(x1, y1, x2, y2, color, opacity=1.0):
	x = x1
	y = y1
	if(x1 > x2):
		x = x2
	if(y1 > y2):
		y = y2
	width = abs(x2 - x1)
	height = abs(y2 - y1)
	if(width == 0):
		width = 1
		# height -= 1
	elif(height == 0):
		height = 1
		# width -= 1

	new_line = document.createElementNS('http://www.w3.org/2000/svg', 'rect')
	new_line.setAttribute('x', f"{x}")
	new_line.setAttribute('y', f"{y}")
	new_line.setAttribute('width', f"{width}")
	new_line.setAttribute('height', f"{height}")
	new_line.setAttribute('opacity', f"{opacity}")
	new_line.setAttribute('style', f"stroke:{color};")
	document.getElementById('svg-drawing').appendChild(new_line)
	return new_line

def draw_lines(tree, person, excluded = ""):
	my_x = tree[person]["x"]
	my_y = tree[person]["y"]
	offset = (1/8) * x_increments

	littles_list = tree[person]["littles"].copy()
	if excluded in littles_list:
		littles_list.remove(excluded)

	# For littles
	middle_y = my_y + 1.5 * y_increments
	if(len(littles_list) > 0):
		vert_line = draw_line_between(my_x, my_y+(NODE_HEIGHT/2), my_x, middle_y, "black") 
		far_left_x = tree[ littles_list[0] ]["x"]
		far_right_x = tree[ littles_list[-1] ]["x"]
		horiz_line = draw_line_between(far_left_x, middle_y, far_right_x, middle_y, "black")

		for little in tree[person]["littles"]:
			if little == excluded:
				continue

			tree[little]["lines"].append([vert_line, my_y+(NODE_HEIGHT/2), middle_y])
			tree[little]["lines"].append([horiz_line, middle_y, middle_y])

			my_line = draw_line_between(tree[little]["x"], middle_y, tree[little]["x"], tree[little]["y"]-(NODE_HEIGHT/2), "black")
			tree[little]["lines"].append([my_line, middle_y, tree[little]["y"]-(NODE_HEIGHT/2)])
			if len(tree[little]["parent_ghost_nodes"]) > 0:
				draw_line_between(tree[little]["x"] - offset, tree[little]["parent_ghost_nodes"][0]["y"] + (NODE_HEIGHT/2), tree[little]["x"] - offset, tree[little]["y"] - (NODE_HEIGHT/2), "green", opacity=GHOST_LINE_OPACITY)
			if(len(tree[little]["littles"]) > 0):
				draw_lines(tree, little)

	# For bigs
	middle_y = my_y - 1.5*y_increments	
	if(len(tree[person]["bigs"]) > 0):
		draw_line_between(my_x, my_y-(NODE_HEIGHT/2), my_x, middle_y, "blue")
		far_left_x = tree[ tree[person]["bigs"][0] ]["x"] + offset
		far_right_x = tree[ tree[person]["bigs"][-1] ]["x"] + offset
		if(tree[person]["x"] > far_right_x):
			far_right_x = tree[person]["x"]
		draw_line_between(far_left_x, middle_y, far_right_x, middle_y, "blue")
		for big in tree[person]["bigs"]:
			draw_line_between(tree[big]["x"] + offset, middle_y, tree[big]["x"] + offset, tree[big]["y"] + (NODE_HEIGHT/2), "blue")
			draw_lines(tree, big, excluded=person)
