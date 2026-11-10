# This has the logic for animating the nodes when hovered over.

from svgnodes import NODE_HEIGHT, NODE_WIDTH, STROKE_WIDTH
from draw import main_root, MAX_QUEUE_SIZE, GHOST_RECT_OPACITY
from collections import deque
from pyscript import document

# TODO simple lines!
# TODO case with 3 or more bigs for ghost parents and top_big


# TODO Elliot case: not necessary i think but it will look a lot nicer on tree. it is an edge case tho so maybe we wont run into it too much

# Constants
MAX_QUEUE_SIZE = 100
REAL_LINE_CONNECT_COLOR = "red"
ANIMATED_GHOST_RECT_OPACITY = 0.9

# Global variables to be used for animations.
info_box = None
animated = deque([], MAX_QUEUE_SIZE)

# Creates an info box.
# IDK if necessary; Kyle question for now
def make_info_box(text, x, y):
	# Create div holder
	holder = document.createElementNS('http://www.w3.org/2000/svg', 'foreignObject'); 
	holder.setAttribute('width', f"100px")
	holder.setAttribute('height', f"100px")
	holder.setAttribute('x', f'{x+100/4}')
	holder.setAttribute('y', f'{y-NODE_HEIGHT*3/2}')
	
	# create text content
	newTextContent = document.createElement('DIV')
	newTextContent.innerHTML = text
	# newTextContent.setAttribute("style", f" \
	# 	display: table-cell; \
	# 	vertical-align: middle; \
	# 	font-size: 11px; \
	# ")
	newTextButton = document.createElement('BUTTON')
	newTextButton.innerHTML = "Go"

	# create text holder
	newTextContainer = document.createElement('DIV')
	newTextContainer.setAttribute("style", f"\
		width: 100px; \
		height: 100px; \
		border: 1px solid green; \
		display: table; \
		width: {NODE_WIDTH}px; \
		height: {NODE_HEIGHT}px; \
		text-align: center; \
	")

	# append text to content and content to div holder
	newTextContainer.appendChild(newTextContent)
	newTextContainer.appendChild(newTextButton)
	holder.appendChild(newTextContainer)
	# nodes are lists of [rectangle, text_content]
	document.getElementById("svg-drawing").appendChild(holder)
	return holder
def update_box(text, x, y):
	global info_box
	if(info_box != None):
		document.getElementById("svg-drawing").removeChild(info_box)
	info_box = make_info_box(text, x, y)

# These are the behaviors when a real / ghost node is hovered.
# We can change behavior. Current behavior displays the path to the root node using the available tree.
# Parameters are self explanitory except for e.
# 		e {Event Object} - HTML DOM object that we don't need to use W
def real_mouseover_event(e, tree, person):
	resetAnimations()
	animateNode(tree[person]["my_node"], tree[person]["y"])
	animateLines(tree[person]["lines"])
	animateAllOtherNodes(tree, person, animated, "", main_root)

# NOTE 	For ghost mouseover, current behavior requires that person
# 		also be animated as it gets us closer to the root node.
def ghost_mouseover_event(e, tree, person, ghost_dict):
	resetAnimations()	
	animateNode(ghost_dict["my_node"], ghost_dict["y"], ghost=True)
	if(ghost_dict["name"] in tree and tree[ghost_dict["name"]]["visited"] == True):
		animateNode(tree[ghost_dict["name"]]["my_node"], tree[ghost_dict["name"]]["y"])
	animateLines(ghost_dict["lines"])
	animateLines(tree[person]["lines"])
	animateNode(tree[person]["my_node"], tree[person]["y"])
	animateAllOtherNodes(tree, person, animated, "", main_root)

# Creates an SVG animation and appends it to (elem).
# Parameters:
#		elem {SVG DOM object} - half a node. either a background rect or content.
#		OG_y {Number} - original Y of the node.x
# NOTE The Y does not change in the tree dict, and goes back to normal when the animation is removed.
# NOTE everytime an animation is added, append it to the (animated) queue so it can eventually be removed.
# Returns the animation element.
ANIMATION_OFFSET = 2
def addAnimation(elem, OG_y):
	animation = document.createElementNS('http://www.w3.org/2000/svg', 'animate'); 
	animation.setAttribute('attributeName', "y")
	animation.setAttribute('dur', "0.05s")
	animation.setAttribute('from', f"{OG_y-NODE_HEIGHT/2}")
	animation.setAttribute('to', f'{OG_y-NODE_HEIGHT/2 - ANIMATION_OFFSET}')
	animation.setAttribute('fill', 'freeze')
	elem.appendChild(animation)
	animation.beginElement()
	return animation

# Animates the line
# The "animation" is just changing the color of the line
# Parameters:
#		line {SVG Element} - line we want to animate
#		color {String} - the new color we want to give the line
#		horizontal {[] | [x1, x2]} - list of x1 and x2 if line is horizontal, nothing if vertical
def addLineAnimation(line, color, horizontal):
	if(len(horizontal) == 2):
		line.setAttribute('x1', f'{horizontal[0] - STROKE_WIDTH/2}')
		line.setAttribute('x2', f'{horizontal[1] + STROKE_WIDTH/2}')
	line.setAttribute('style', f'stroke: {color}; stroke-width: {STROKE_WIDTH*2};')

# Gives animations and shadows to given node.
# Paramenters
#		node {HTML Object list} - node we want to animate
#		y {Number} - Y of given node.
def animateNode(node, y, ghost=False):
	animation = addAnimation(node[0], y)
	animated.append([node[0], animation])
	addShadow(node[0], ghost)
	animation = addAnimation(node[1], y)
	animated.append([node[1], animation])

# Animates each line in the line list
# The (animated) queue is used for resetting the animations
def animateLines(line_list):
	for line in line_list:
		addLineAnimation(line[0], REAL_LINE_CONNECT_COLOR, line[2])
		animated.append(line) # line[0] is html elem, line[1] is string with color, line[2] is list of either length 0 or 2 depending on if line is horizontal or not.

# Removes the SVG animations and shadow filters from the global (animated) queue.
def resetAnimations():
	while(len(animated) > 0):
		front = animated.popleft()
		elem = front[0]
		animation = front[1]
		if(isinstance(animation, str)): # is a line
			resetLine(elem, animation, front[2])
		elif(isinstance(animation, bool)): # is an opacity change for ghost nodes
			elem.setAttribute("opacity", f"{GHOST_RECT_OPACITY}")
		else: # is not a line
			resetShadow(elem) # code is used on elements that don't have shadows; could be optimized
			elem.removeChild(animation)

# Could be unnecessary depending on the way we want our hovers to work.
def animateAllMyNodes(tree, person, only_including=""):
	tree[person]["animated"] = True
	person_dict = tree[person]
	if(person_dict["visited"]):
		animateNode(person_dict["my_node"], person_dict["y"])
	animateLines(person_dict["lines"])
	
	# animate ghost bigs
	for ghost in person_dict["parent_ghost_nodes"]:
		if(only_including != "" and only_including == ghost["name"]):
			animateNode(ghost["my_node"], ghost["y"])
			return
	# animate ghost littles
	for ghost in person_dict["child_ghost_nodes"]:
		if(only_including != "" and only_including == ghost["name"]):
			animateNode(ghost["my_node"], ghost["y"])
			return

# We can change function based on behavior we want.
# Current behavior is to only go up until we reach a top_big, then go down to move to the root.
def animateAllOtherNodes(tree, person, animated, previous, end):	
	if(person == end):
		return
	# append names of ghost nodes so we don't treat them like real nodes
	dont_include = []
	for ghost in tree[person]["child_ghost_nodes"]:
		dont_include.append(ghost["name"])
	for ghost in tree[person]["parent_ghost_nodes"]:
		dont_include.append(ghost["name"])

	if(tree[person]["top_big"]):
		for little in tree[person]["littles"]:
			if(little != previous  and little not in dont_include):
				if(tree[little]["top_big"]):
					animateAllMyNodes(tree, little)
					animateAllOtherNodes(tree, little, animated, previous, end)
					break
		return

	for big in tree[person]["bigs"]:
		if(big != previous and big not in dont_include):
			animateAllMyNodes(tree, big)
			animateAllOtherNodes(tree, big, animated, previous, end)
			break
	return

# Gives (elem) the shadow filter seen in the svg-drawing
def addShadow(elem, change_opacity):
	if(change_opacity):
		elem.setAttribute("opacity", f"{ANIMATED_GHOST_RECT_OPACITY}")
		animated.append([elem, True])
	elem.setAttribute("filter", "url(#shadow)")

# Reverts the styling from a line animation.
def resetLine(line, og_color, horizontal):
	if(len(horizontal) == 2):
		line.setAttribute('x1', f'{horizontal[0]}')
		line.setAttribute('x2', f'{horizontal[1]}')
	line.setAttribute("style", f"stroke: {og_color}; stroke-width: {STROKE_WIDTH};")

# Removes the shadow filter from (elem)
def resetShadow(elem):
	elem.setAttribute("filter", "")

