# This is the main drawing file. Has the logic for positioning nodes on the svg.

# Constants
MAX_QUEUE_SIZE = 100

# Colors
DEFAULT_COLOR = "orange"
GHOST_PARENT_COLOR = "#93e0f5"
NORMAL_GHOST_COLOR = "#f56262"
ROOT_COLOR = "#b869f0"

# Opacities
GHOST_TEXT_OPACITY = 0.9
GHOST_RECT_OPACITY = 0.6
GHOST_LINE_OPACITY = 0.7

# Determines distances between nodes on trees
x_increments = 100 
y_increments = 100 

# Global Variable used throughout code
main_root = None

import animation
import svgnodes

from collections import deque
from pyscript import document
from js import Event

# Draws the subtree of the root given in the tree
#	Parameters:
# 		tree {Hash Map / Dict} - Has all the information about people in our tree
# 		person {String} - name of the person we are processing
#		excluding { "" | String} - person to exclude from drawing of subtree.
#		color {String | HEX Color} - color that (person)'s node will be drawn with
#	Notes:
#		This is a recursive function that operates in preorder.
#		This function draws the ghost parents for (person)'s littles.
#	ASSUMPTION: 
# 		- Ghost child nodes are ALWAYS placed to the RIGHT of real child nodes.
# 	Returns the position of the farthest right node in the subtree.
def draw_tree_down(tree, person, excluding="", color=DEFAULT_COLOR):
	# Create node if it has not already been created and store it in (html_node)
	html_node = None
	if(tree[person]["visited"] == False):
		tree[person]["visited"] = True
		html_node = svgnodes.make_node(person, color)
		tree[person]["my_node"] = html_node
		add_real_mouseover_event(tree, person)
		add_click_event(tree, person=person)
	else:
		html_node = tree[person]["my_node"]

	# Get an array of unvisited littles and visited littles
	unvisited_lils_length = len(tree[person]["littles"])
	unvisited_littles = tree[person]["littles"].copy()
	visited_littles = [] # place visited littles in another array to make a parent ghost node
	i = unvisited_lils_length - 1
	while(i >= 0):
		little = tree[unvisited_littles[i]]
		# if we are excluding someone, make sure they are not in either visited or unvisited list
		if(unvisited_littles[i] == excluding): 
			unvisited_littles.pop(i)
		elif(little["visited"]):
			visited_littles.append(unvisited_littles.pop(i))
		i -= 1
	unvisited_lils_length = len(unvisited_littles) 


	# If we have no littles, skip the recursion and alignment stuff
	total_length = unvisited_lils_length + len(visited_littles)
	if(total_length == 0):
		svgnodes.update_node_position(tree, person)
		return tree[person]["x"]

	# If we have littles, operate recursively throughout the tree.
	my_starting_x = tree[person]["x"]
	begin_x = my_starting_x # used to store where the next tree should start being built
	lil_index = 0
	# iterate on unvisited lils only first.
	while lil_index < unvisited_lils_length:
		little = unvisited_littles[lil_index]
		tree[little]["x"] = begin_x
		tree[little]["y"] = tree[person]["y"] + 2 * y_increments
		
		begin_x = draw_tree_down(tree, little)
		begin_x += 1 * x_increments
		# (begin_x) is now equal to where the next tree should start being built.

		# Check if a sib of (little) became visited. If they are, remove them from (unvisited_littles)
		i = unvisited_lils_length - 1
		stop_point = lil_index
		while(i > stop_point):
			lil_dict = tree[unvisited_littles[i]]
			if(lil_dict["visited"]):
				visited_littles.append(unvisited_littles.pop(i))
			i -= 1
		unvisited_lils_length = len(unvisited_littles)

		# Check if littles have bigs that are not (person); if they do, make parent ghost nodes
		if(len(tree[little]["bigs"]) > 1):
			ghost_x_inc = 0
			for big in tree[little]['bigs']:
				if(big != person):
					new_ghost_node = {
						"name": big,
						"my_node": svgnodes.make_node(big, GHOST_PARENT_COLOR, GHOST_RECT_OPACITY),
						"x": tree[little]["x"] + (ghost_x_inc * x_increments),
						"y": tree[little]["y"] - 1 * y_increments, 
						"lines": []
					}
					add_ghost_mouseover_event(tree, little, new_ghost_node)
					add_click_event(tree, person=little, ghost_dict=new_ghost_node)
					tree[little]["parent_ghost_nodes"].append(new_ghost_node)
					svgnodes.set_node_position(new_ghost_node["my_node"], new_ghost_node["x"], new_ghost_node["y"])
					ghost_x_inc += 1
			# If we had more than one ghost big, make sure to center (person) and their children under the nodes.
			if(ghost_x_inc > 1):
				distance_between_ghosts = (ghost_x_inc - 1) * x_increments 
				begin_x += distance_between_ghosts
				offset = distance_between_ghosts / 2
				tree[little]["x"] += offset
				offset_littles_x(tree, little, offset)
				svgnodes.update_node_position(tree, little)
		lil_index += 1

	# If the littles ARE visited, it means they are somewhere else in the tree. Make a child ghost node instead at the far right of the subtree.
	for little in visited_littles:
		new_ghost_node = {
			"name": little,
			"my_node": svgnodes.make_node(little, NORMAL_GHOST_COLOR, GHOST_RECT_OPACITY),
			"x": begin_x,
			"y": tree[person]["y"] + 2 * y_increments, 
			"lines": []
		}
		add_ghost_mouseover_event(tree, person, new_ghost_node)
		add_click_event(tree, person=person, ghost_dict=new_ghost_node)
		tree[person]["child_ghost_nodes"].append(new_ghost_node)
		svgnodes.set_node_position(new_ghost_node["my_node"], new_ghost_node["x"], new_ghost_node["y"])
		begin_x += 1 * x_increments

	# Align (person) over their littles
	my_far_left_x = tree[person]["x"]
	my_far_right_x = tree[person]["x"]

	if unvisited_lils_length > 0:
		my_far_left_x = tree[ unvisited_littles[0] ]["x"]
		my_far_right_x = tree[ unvisited_littles[-1] ]["x"]

	if len(tree[person]["child_ghost_nodes"]) > 0:
		my_far_right_x = tree[person]["child_ghost_nodes"][-1]["x"]

	tree[person]["x"] = (my_far_left_x + my_far_right_x) / 2

	svgnodes.update_node_position(tree, person)

	farthest_right_x = begin_x - 1 * x_increments
	return farthest_right_x

# Offsets all nodes in the subtree of (person) by (amt)
#	Parameters:
# 		tree {Hash Map / Dict} - Has all the information about people in our tree
# 		person {String} - name of the person we are processing
#		amt {Number | 0} - amount used for offsetting nodes.
#		not_including {String | ""} - name of little to not offset.
# Returns the farthest_right_x of the nodes operated on.
def offset_littles_x(tree, person, amt, not_including=""):
	farthest_right_x = tree[person]["x"]

	# If we find more people that we don't want to include, add them to a list.
	skip_list = []
	skip_list.append(not_including)

	# Update person's ghost children and add them to (skip_list) so their real node is not offset
	for ghost in tree[person]["child_ghost_nodes"]:
		ghost["x"] += amt
		if(ghost["x"] > farthest_right_x):
			farthest_right_x = ghost["x"]	
		svgnodes.set_node_position(ghost["my_node"], ghost["x"], ghost["y"])
		skip_list.append(ghost["name"])

	# Offset each little’s x in (person)'s littles list by (amt)
	for little in tree[person]["littles"]:
		# Avoid anyone not created yet or in skip_list
		if(not tree[little]["visited"] or (little in skip_list)): 
			continue
		# Offset little
		tree[little]["x"] += amt
		if(tree[little]["x"] > farthest_right_x):
			farthest_right_x = tree[little]["x"]
		svgnodes.set_node_position(tree[little]["my_node"], tree[little]["x"], tree[little]["y"])

		# Update (little)'s ghost parents
		for ghost in tree[little]["parent_ghost_nodes"]:
			ghost["x"] += amt
			svgnodes.set_node_position(ghost["my_node"], ghost["x"], ghost["y"])

		# Recurse for real children
		if(len(tree[little]["littles"]) > 0 and tree[little]["visited"]):
			far_right_x = offset_littles_x(tree, little, amt)
			if(far_right_x > farthest_right_x):
				farthest_right_x = far_right_x
	return farthest_right_x

# Draws tree upwards
# Parameters:
# 		tree {Hash Map / Dict} - Has all the information about people in our tree
#		queue {collections.deque} - Holds data of what to operate on next. See draw_full_tree() for description of data.
# 		direction {-1 | +1} - Direction of drawing, either left or right
#		outward_offset {Number} - Offset generated from the previous iteration of BFS.
# Notes:
#		- Queue operations are append() to add and popleft() to remove.
#		- Queue has data of [current_person, who_they_came_from]
#		- "top_big" attribute means they are a part of the "fanning" pattern at the top of the tree.
#		- IMPORTANT there is a small chance of overlap occurring on the branch closest to (person), but extremely unlikely.
def draw_tree_up(tree, queue, direction, outward_offset):
	front = queue.popleft()
	person = front[0]
	current_little = front[1]

	# Check for already created bigs in (queue). If they were already created, make a ghost parent for (current_little) instead of a real one.
	if(tree[person]["top_big"]):
		num_ghosts = len(tree[person]["parent_ghost_nodes"])
		ghost_dict = None
		if(num_ghosts > 0):
			ghost_index = 0
			# Branches ghost_bigs towards the center, removing MOST cases of overlap.
			while(ghost_index < num_ghosts):
				ghost_dict = tree[person]["parent_ghost_nodes"][ghost_index]
				ghost_dict["x"] -= 0.5 * x_increments * direction
				svgnodes.set_node_position(ghost_dict["my_node"], ghost_dict["x"], ghost_dict["y"])
				ghost_index += 1

		# If we have no other Ghost Bigs, use current x as ghost_parent's x.
		your_x = 0
		if(ghost_dict == None):
			your_x = tree[current_little]["x"]
		else:
			your_x = ghost_dict["x"] + 1 * x_increments

		# Create the node.
		new_ghost_node = {
			"name": person,
			"my_node": svgnodes.make_node(person, NORMAL_GHOST_COLOR, GHOST_RECT_OPACITY),
			"x": your_x,
			"y": tree[current_little]["y"] - 1 * y_increments, 
			"lines": []
		}
		add_ghost_mouseover_event(tree, current_little, new_ghost_node)
		add_click_event(tree, person=current_little, ghost_dict=new_ghost_node)
		tree[current_little]["parent_ghost_nodes"].append(new_ghost_node)
		svgnodes.set_node_position(new_ghost_node["my_node"], new_ghost_node["x"], new_ghost_node["y"])
		# Check if the queue is done; if not, continue like normal.
		if(len(queue) > 0):
			draw_tree_up(tree, queue, direction, outward_offset = outward_offset)
		return
	
	# Draw (person)'s subtree, making sure to start from the right of the far_right node.
	tree[person]["x"] += outward_offset
	starting_x = tree[person]["x"]
	far_x = draw_tree_down(tree, person, excluding=current_little)
	tree[person]["top_big"] = True

	# If we are moving left, offset all nodes to the left by the distance travelled and change out to give the far left x.
	total_offset = 0
	out = far_x
	if(direction < 0):
		total_offset = starting_x - far_x
		tree[person]["x"] += total_offset
		out = starting_x + total_offset
		offset_littles_x(tree, person, total_offset, not_including=current_little)
	svgnodes.update_node_position(tree, person)

	# Add nodes to the queue in the direction they are placed in dicts.
	bigs_length = len(tree[person]["bigs"])
	if(direction < 0): # moving left
		bigIndex = bigs_length - 1
	else: # moving right
		bigIndex = 0
	ghost_x_inc = 0
	while(0 <= bigIndex and bigIndex < bigs_length):
		big = tree[person]["bigs"][bigIndex]
		if(not tree[big]["visited"]):
			tree[big]["y"] = tree[person]["y"] - (2 * y_increments)
			queue.append([big, person])
		else:
			# If (big) is visited, make a ghost node.
			new_ghost_node = {
				"name": big,
				"my_node": svgnodes.make_node(big, NORMAL_GHOST_COLOR, GHOST_RECT_OPACITY),
				"x": tree[person]["x"] + (ghost_x_inc * x_increments * direction),
				"y": tree[person]["y"] - 1 * y_increments, 
				"lines": []
			}
			add_ghost_mouseover_event(tree, person, new_ghost_node)
			add_click_event(tree, person=person, ghost_dict=new_ghost_node)
			tree[person]["parent_ghost_nodes"].append(new_ghost_node)
			svgnodes.set_node_position(new_ghost_node["my_node"], new_ghost_node["x"], new_ghost_node["y"])
			ghost_x_inc += 1
		bigIndex += direction

	# If there were more than 1 ghost bigs, offset (person) and thier littles
	if ghost_x_inc > 0:
		ghost_offset = (ghost_x_inc - 1) * x_increments / 2 * direction
		tree[person]["x"] += ghost_offset
		svgnodes.update_node_position(tree, person)
		offset_littles_x(tree, person, ghost_offset, not_including=current_little)

	# Go next in queue
	# outward_offset is the far right/left x plus 1 increment
	if(len(queue) > 0):
		draw_tree_up(tree, queue, direction, outward_offset = out + (direction * x_increments))
	return

# Sets up the root node and immediate bigs for drawing.
# Parameters are self-explanatory
# NOTE 	The reason why we make immediate parent nodes here is because during 
# 		the draw_tree_up, we want a more balanced tree. If we didn't visit
#		the node here and the immediate right parents are found in the left
# 		parent's tree (2 bigs pick up 2 littles case), it would be extremely
#		unbalanced. Can be removed if we improve BFS by alternating directions.
# NOTE Queues have data of [current_person, who_they_came_from]
# Returns the x position of (person)
def draw_full_tree(tree, person):
	# Make root node.
	tree[person]["visited"] = True
	tree[person]["x"] = 0
	tree[person]["y"] = 0
	html_node = svgnodes.make_node(person, f"{ROOT_COLOR}")
	html_node[0].setAttribute("class", "main-root")
	tree[person]["my_node"] = html_node
	tree[person]["top_big"] = True
	add_real_mouseover_event(tree, person)

	# Set the main_root for animations
	global main_root
	main_root = person

	# Draw littles and place root in middle of subtree.
	starting_x = tree[person]["x"] 
	ending_x = draw_tree_down(tree, person, color="red")
	total_offset = ending_x - starting_x
	# print(f"total_offset: {total_offset}")
	# tree[person]["x"] = (ending_x + starting_x) / 2 
	svgnodes.update_node_position(tree, person)

	# Prepare to draw bigs.
	bigs_length = len(tree[person]["bigs"])
	if(bigs_length == 1):
		# draw big to the right
		rightQueue = deque([], MAX_QUEUE_SIZE)
		bigIndex = 0
		while bigIndex < bigs_length:
			big = tree[person]["bigs"][bigIndex]

			# Give position
			tree[big]["y"] = tree[person]["y"] - (2 * y_increments)

			# Make node
			tree[big]["visited"] = True
			html_node = svgnodes.make_node(big, DEFAULT_COLOR)
			svgnodes.set_node_position(html_node, tree[big]["x"], tree[big]["y"])
			tree[big]["my_node"] = html_node
			add_real_mouseover_event(tree, big)
			add_click_event(tree, person=big)

			# Append to Queue
			rightQueue.append([big, person])
			bigIndex += 1

		# The BFS could alternate between going left and right to have a more balanced tree.
		draw_tree_up(tree, rightQueue, direction = +1, outward_offset = starting_x + (1 * x_increments) + total_offset)
	
	if(bigs_length >= 2):
		# Add bigs into 2 separate queues, one going left and one going right
		# Split bigs down the middle to support people with more than 2 bigs.
		middle_index = bigs_length // 2 
		leftQueue = deque([], MAX_QUEUE_SIZE)
		rightQueue = deque([], MAX_QUEUE_SIZE)

		# Add Left Bigs to Queue.
		bigIndex = middle_index - 1
		while bigIndex >= 0:
			big = tree[person]["bigs"][bigIndex]

			# Give position
			tree[big]["y"] = tree[person]["y"] - (2 * y_increments)

			# Make node
			tree[big]["visited"] = True
			html_node = svgnodes.make_node(big, DEFAULT_COLOR)
			svgnodes.set_node_position(html_node, tree[big]["x"], tree[big]["y"])
			tree[big]["my_node"] = html_node
			add_real_mouseover_event(tree, big)
			add_click_event(tree, person=big)

			# Append to Queue
			leftQueue.append([big, person])
			bigIndex -= 1

		# Add Right Bigs to Queue
		bigIndex = middle_index
		while bigIndex < bigs_length:
			big = tree[person]["bigs"][bigIndex]

			# Give position
			tree[big]["y"] = tree[person]["y"] - (2 * y_increments)

			# Make node
			tree[big]["visited"] = True
			html_node = svgnodes.make_node(big, DEFAULT_COLOR)
			svgnodes.set_node_position(html_node, tree[big]["x"], tree[big]["y"])
			tree[big]["my_node"] = html_node
			add_real_mouseover_event(tree, big)
			add_click_event(tree, person=big)

			# Append to Queue
			rightQueue.append([big, person])
			bigIndex += 1

		# The BFS could alternate between going left and right to have a more balanced tree.
		draw_tree_up(tree, leftQueue, direction = -1, outward_offset = starting_x - (1 * x_increments))
		draw_tree_up(tree, rightQueue, direction = +1, outward_offset = starting_x + (1 * x_increments) + total_offset)
	# DRAW LINES
	svgnodes.draw_lines(tree, person)
	
	return tree[person]["x"]


# Gives mouseover behavior to (person)'s node
def add_real_mouseover_event(tree, person):
	tree[person]["my_node"][1].addEventListener("mouseover", lambda e: animation.real_mouseover_event(e, tree, person))

# Gives mouseover behavior to (ghost_dict)'s node
def add_ghost_mouseover_event(tree, real_person, ghost_dict):
	ghost_dict["my_node"][1].addEventListener("mouseover", lambda e: animation.ghost_mouseover_event(e, tree, real_person, ghost_dict))

# Gives click behavior to either person or ghost
def add_click_event(tree, person=None, ghost_dict=None):
	if(ghost_dict == None):
		tree[person]["my_node"][1].addEventListener("click", lambda e: click_event(e, tree, person=person))
		tree[person]["my_node"][1].addEventListener("touchstart", lambda e: click_event(e, tree, person=person))
	else:
		ghost_dict["my_node"][1].addEventListener("click", lambda e: click_event(e, tree, person=person, ghost_dict=ghost_dict))
		ghost_dict["my_node"][1].addEventListener("touchstart", lambda e: click_event(e, tree, person=person, ghost_dict=ghost_dict))

# Variables for animation for SVG fading behavior set in a click_event()
iteration_count = 0
animation_x = 0
input_name = None

# Adds event listeners to the svg 
def prepare_svg():
	svg = document.getElementById("svg-drawing")
	svg.addEventListener("animationiteration", switchTree)
	svg.addEventListener("animationend", switchTree)

# On a click, make a new tree with clicked person as the root.
def click_event(e, tree, person=None, ghost_dict=None):
	# Checks done for mobile compatibility
	if(e != None):
		e.preventDefault()
		e.stopPropagation()

	# Set variables to be used by switchTree().
	if(ghost_dict == None):
		global tree_dict
		global input_name
		tree_dict = tree
		input_name = person
	else:
		global tree_dict
		global input_name
		tree_dict = tree
		input_name = ghost_dict["name"]

	# Add animation to the svg
	svg = document.getElementById("svg-drawing")
	svg.classList.add("SVGanimate")

# Switches the tree to the person clicked
def switchTree(e):
	global iteration_count
	global animation_x
	iteration_count += 1
	svg = document.getElementById("svg-drawing")
	if(iteration_count == 1):
		animation.resetAnimations()
		svgnodes.removeNodes()
		resetDict(tree_dict)
		if(tree_dict != None and input_name != None):
			animation_x = draw_full_tree(tree_dict, input_name)
		# set value attribute of drawing for animationiteration event in zoom.js
		newEvent = Event.new("setsvgcenter")
		print(f"pyscript says {animation_x}")
		svg.setAttribute("value", f"{animation_x}")
		svg.dispatchEvent(newEvent)
	elif(iteration_count == 2):
		iteration_count = 0
		svg.classList.remove("SVGanimate")


# Reset all the used/changed values in the dict
def resetDict(tree):
	for person in tree:
		tree[person]["x"] = 0
		tree[person]["y"] = 0
		if(tree[person]["visited"]):
			tree[person]["my_node"] = None
		tree[person]["visited"] = False
		tree[person]["parent_ghost_nodes"] = []
		tree[person]["child_ghost_nodes"] = []
		tree[person]["top_big"] = False
