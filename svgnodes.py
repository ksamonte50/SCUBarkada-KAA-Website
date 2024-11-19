# This has the building blocks for svg content using the DOM

# TODO draw_tree_down lil 1 and lil 2 animation on lil 1 2 tree

# TODO case with lil 1 1 as root BAD

# Constants
NODE_WIDTH = 75
NODE_HEIGHT = 50
STROKE_WIDTH = 2

CHILD_LINE_COLOR = "black"
REAL_PARENT_LINE_COLOR = "#ff7b00"
GHOST_PARENT_LINE_COLOR = "gray"

REAL_LINE_CONNECT_COLOR = "#fdb833"

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
		overflow: hidden; \
		color: white; \
	")

	# create text holder
	newTextContainer = document.createElement('DIV')
	newTextContainer.setAttribute("style", f"\
		display: table; \
		width: {NODE_WIDTH}px; \
		height: {NODE_HEIGHT}px; \
		text-align: center; \
		cursor: pointer; \
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

def removeNode(node):
	drawing = document.getElementById("svg-drawing")
	drawing.removeChild(node[0])
	drawing.removeChild(node[1])


# Removes Nodes From SVG
def removeNodes():
	drawing = document.getElementById("svg-drawing")
	while(drawing.firstChild):
		drawing.removeChild(drawing.lastChild)
	addFilters()


# Adds this HTML to the SVG after all nodes are removed:
# <defs id = "defs">
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
	defs.setAttribute("id", "defs")
	nodeFilter = document.createElementNS('http://www.w3.org/2000/svg', 'filter')
	nodeFilter.setAttribute("id", "shadow")
	nodeFilter.setAttribute("width", "125")
	nodeFilter.setAttribute("height", "125")
	nodeShadow = document.createElementNS('http://www.w3.org/2000/svg', 'feDropShadow')
	nodeShadow.setAttribute("dx", "")
	nodeShadow.setAttribute("dy", "4")
	nodeShadow.setAttribute("stdDeviation", "2.5")
	nodeFilter.appendChild(nodeShadow)

	lineFilter = document.createElementNS('http://www.w3.org/2000/svg', 'filter')
	lineFilter.setAttribute("id", "line-shadow")
	lineFilter.setAttribute("width", "125")
	lineFilter.setAttribute("height", "125")
	lineShadow = document.createElementNS('http://www.w3.org/2000/svg', 'feDropShadow')
	lineShadow.setAttribute("dx", "2")
	lineShadow.setAttribute("dy", "4")
	lineShadow.setAttribute("stdDeviation", "2.5")
	# lineBlur = document.createElementNS('http://www.w3.org/2000/svg', 'feGaussianBlur')
	# lineBlur.setAttribute("in", "SourceGraphic")
	# lineBlur.setAttribute("stdDeviation", "0.9")

	lineFilter.appendChild(lineShadow)
	# lineFilter.appendChild(lineBlur)

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
	new_line = document.createElementNS('http://www.w3.org/2000/svg', 'line')
	new_line.setAttribute('x1', f"{x1}")
	new_line.setAttribute('y1', f"{y1}")
	new_line.setAttribute('x2', f"{x2}")
	new_line.setAttribute('y2', f"{y2}")
	new_line.setAttribute('opacity', f"{opacity}")
	new_line.setAttribute('style', f"stroke:{color}; stroke-width: {STROKE_WIDTH};")

	defs = document.getElementById('defs')
	document.getElementById('svg-drawing').insertBefore(new_line, defs)
	return new_line

def draw_lines(tree, person, excluded = "", top_big_offset = 0):
	my_x = tree[person]["x"]
	my_y = tree[person]["y"]
	half_stroke_width = STROKE_WIDTH/2
	offset = (1/8) * x_increments

	littles_list = tree[person]["littles"].copy()
	# exclude top_big little	
	if excluded in littles_list:
		littles_list.remove(excluded)
	# exclude ghost littles 
	for ghost in tree[person]["child_ghost_nodes"]: 
		if ghost["name"] in littles_list:
			littles_list.remove(ghost["name"])
	
	# For littles
	middle_y = my_y + 1.5 * y_increments
	if(len(littles_list) > 0 or len(tree[person]["child_ghost_nodes"]) > 0): # check if person has littles
		vert_line = draw_line_between(my_x, my_y, my_x, middle_y, f"{CHILD_LINE_COLOR}")	
		far_left_x = my_x
		far_right_x = my_x

		if(len(littles_list) > 0):
			far_left_x = tree[ littles_list[0] ]["x"]
			far_right_x = tree[ littles_list[-1] ]["x"]
		
		if(len(tree[person]["child_ghost_nodes"]) > 0):
			if(len(littles_list) == 0):
				far_left_x = tree[person]["child_ghost_nodes"][0]["x"]
			far_right_x = tree[person]["child_ghost_nodes"][-1]["x"]
			
		if(tree[person]["x"] > far_right_x):
			far_right_x = tree[person]["x"]
		if(tree[person]["x"] < far_left_x):
			far_left_x = tree[person]["x"]
		
		horiz_line = draw_line_between(far_left_x - half_stroke_width, middle_y, far_right_x + half_stroke_width, middle_y, f"{CHILD_LINE_COLOR}")
		
		# Real Littles
		for little in littles_list:
			tree[little]["lines"].append([vert_line, f"{CHILD_LINE_COLOR}", []])
			tree[little]["lines"].append([horiz_line, f"{CHILD_LINE_COLOR}", [far_left_x - half_stroke_width, far_right_x + half_stroke_width]])

			my_line = draw_line_between(tree[little]["x"], middle_y, tree[little]["x"], tree[little]["y"], f"{CHILD_LINE_COLOR}")
			tree[little]["lines"].append([my_line, f"{CHILD_LINE_COLOR}", []])

			# Draw lines for ghost parents of littles
			if len(tree[little]["parent_ghost_nodes"]) > 0:
				y = tree[little]["parent_ghost_nodes"][0]["y"]+(3 * NODE_HEIGHT/4)
				temp_vert_line = draw_line_between(tree[little]["x"] - offset, y, tree[little]["x"] - offset, tree[little]["y"], f"{GHOST_PARENT_LINE_COLOR}", opacity=GHOST_LINE_OPACITY)
				horiz_needed = True
				temp_far_left_x = tree[little]["parent_ghost_nodes"][0]["x"] - offset
				temp_far_right_x = tree[little]["parent_ghost_nodes"][-1]["x"] - offset
				if(temp_far_left_x == temp_far_right_x):
					horiz_needed = False
				else: 
					temp_horiz_line = draw_line_between(temp_far_left_x - half_stroke_width, y, temp_far_right_x + half_stroke_width, y, f"{GHOST_PARENT_LINE_COLOR}")
				for ghost_dict in tree[little]["parent_ghost_nodes"]:
					ghost_dict["lines"].append([temp_vert_line, f"{GHOST_PARENT_LINE_COLOR}", []])
					if(horiz_needed):
						ghost_dict["lines"].append([temp_horiz_line, f"{GHOST_PARENT_LINE_COLOR}", [temp_far_left_x - half_stroke_width, temp_far_right_x + half_stroke_width]])

					my_line = draw_line_between(ghost_dict["x"] - offset, y, ghost_dict["x"] - offset, ghost_dict["y"]+NODE_HEIGHT/2, f"{GHOST_PARENT_LINE_COLOR}", opacity=GHOST_LINE_OPACITY) 
					ghost_dict["lines"].append([my_line, f"{GHOST_PARENT_LINE_COLOR}", []])

			# recursively draw lines for other littles
			if(len(tree[little]["littles"]) > 0):
				draw_lines(tree, little, excluded=person)

		# Ghost Littles
		for ghost_dict in tree[person]["child_ghost_nodes"]:
			ghost_dict["lines"].append([vert_line, f"{CHILD_LINE_COLOR}", []])
			ghost_dict["lines"].append([horiz_line, f"{CHILD_LINE_COLOR}", [far_left_x - half_stroke_width, far_right_x + half_stroke_width]])

			my_line = draw_line_between(ghost_dict["x"], middle_y, ghost_dict["x"], ghost_dict["y"] - (NODE_HEIGHT/2), f"{CHILD_LINE_COLOR}")
			ghost_dict["lines"].append([my_line, f"{CHILD_LINE_COLOR}", []])
		# if(person == "big 2"):
		# 	exit()

	bigs_list = tree[person]["bigs"].copy()
	# exclude top_big little	
	if excluded in bigs_list:
		bigs_list.remove(excluded)
	# exclude ghost bigs 
	for ghost in tree[person]["parent_ghost_nodes"]: 
		if ghost["name"] in bigs_list:
			bigs_list.remove(ghost["name"])


	# For bigs
	if(top_big_offset == 0):
		middle_y = my_y - 1.5 * y_increments
	else:
		middle_y = my_y - 2 * y_increments + NODE_HEIGHT/2 + top_big_offset
	if((len(bigs_list) > 0 or len(tree[person]["parent_ghost_nodes"]) > 0) and tree[person]["top_big"]):
		far_left_x = my_x
		far_right_x = my_x

		vert_line = None

		if(len(bigs_list) > 0):
			vert_line = draw_line_between(my_x, my_y, my_x, middle_y, f"{REAL_PARENT_LINE_COLOR}")
			if(my_x > tree[bigs_list[0]]["x"]):	
				far_left_x = tree[ bigs_list[0] ]["x"] + offset

			if(my_x < tree[bigs_list[-1]]["x"]):
				far_right_x = tree[ bigs_list[-1] ]["x"] + offset
		
			horiz_line = draw_line_between(far_left_x - half_stroke_width, middle_y, far_right_x + half_stroke_width, middle_y, f"{REAL_PARENT_LINE_COLOR}")
			# if(person == "Joshua Sixto Beltran"):
			# 	print(my_x)
			# 	print(far_right_x)
			# 	print(far_left_x)
			# 	exit()
			
			# Top big real parent nodes
			big_inc = 1
			
			big_count = len(tree[person]["bigs"])
			for big in bigs_list:
				my_line = draw_line_between(tree[big]["x"] + offset, middle_y, tree[big]["x"] + offset, tree[big]["y"], f"{REAL_PARENT_LINE_COLOR}")
				
				tree[big]["lines"].append([vert_line, f"{REAL_PARENT_LINE_COLOR}", []])
				tree[big]["lines"].append([horiz_line, f"{REAL_PARENT_LINE_COLOR}", [far_left_x - half_stroke_width, far_right_x + half_stroke_width]])
				tree[big]["lines"].append([my_line, f"{REAL_PARENT_LINE_COLOR}", []])
				if(tree[big]["top_big"]):
					your_offset = (y_increments - NODE_HEIGHT)/(1+big_count)
					draw_lines(tree, big, excluded=person, top_big_offset=your_offset * big_inc)
					big_inc += 1
				else:
					draw_lines(tree, big, excluded=person)

		# Top big ghost parent nodes
		if(len(tree[person]["parent_ghost_nodes"]) > 0):
			temp_y = ghost["y"]+ (3 * NODE_HEIGHT/4)
			temp_vert_line = draw_line_between(tree[person]["x"] + offset, tree[person]["y"], tree[person]["x"] + offset, temp_y, f"{GHOST_PARENT_LINE_COLOR}")
			horiz_needed = True
			temp_far_left_x = tree[person]["parent_ghost_nodes"][0]["x"] + offset
			temp_far_right_x = tree[person]["parent_ghost_nodes"][-1]["x"] + offset
			if(temp_far_left_x == temp_far_right_x):
				horiz_needed = False
			else:
				temp_horiz_line = draw_line_between(temp_far_left_x - half_stroke_width, temp_y, temp_far_right_x + half_stroke_width, temp_y, f"{GHOST_PARENT_LINE_COLOR}")
			for ghost in tree[person]["parent_ghost_nodes"]:

				my_line = draw_line_between(ghost["x"] + offset, ghost["y"] + NODE_HEIGHT/2, ghost["x"] + offset, ghost["y"]+ (3 * NODE_HEIGHT/4), f"{GHOST_PARENT_LINE_COLOR}")
				if(horiz_needed):
					ghost["lines"].append([temp_horiz_line, f"{GHOST_PARENT_LINE_COLOR}", [temp_far_left_x - half_stroke_width, temp_far_right_x + half_stroke_width]])
				ghost["lines"].append([my_line, f"{GHOST_PARENT_LINE_COLOR}", []])
				ghost["lines"].append([temp_vert_line, f"{GHOST_PARENT_LINE_COLOR}", []])
			