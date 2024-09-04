# This is the main drawing file. Has the logic for positioning nodes on the svg.

# TODO simple lines!
# TODO Elliot case: not necessary i think but it will look a lot nicer on tree. it is an edge case tho so maybe we wont run into it too much

test = {
	"Kyle Samonte": {
		"row": 0,
		"bigs": ['big 3','big 4'],
		# "bigs": [],
		# "littles": [],
		# "littles": ["Joshua Sixto Beltran", "Ryan Lo"],
		# "littles": ["Joshua Sixto Beltran", "Ryan Lo", "Christian Chow"],
		# "littles": ["Alessandro Bischocho", "Christian Chow"],
		"littles": ["Christian Chow", "Joshua Sixto Beltran", "Ryan Lo", "Alessandro Bischocho",],
		# "littles": ["Ryan Lo", "Alessandro Bischocho", "Christian Chow",],
		"x":0,
		"y":0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"animated": False,
		"top_big": False,
	}, 
	"Joshua Sixto Beltran": {
		"row": 0,
		"bigs": ['Sam Solomon','Kyle Samonte', "big 3"],
		# "littles": ['lil 1', 'lil 2'],
		"littles": [],
		"x": 0,
		"y": 0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"animated": False,
		"top_big": False,
	},
	"Ryan Lo":{
		"row": 0,
		"bigs" : ["Adrian Marc Santiago",'Kyle Samonte'],
		"littles": ['lil 3'],
		# "littles": [],
		"x": 0,
		"y": 0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"animated": False,
		"top_big": False,
	},
	"Alessandro Bischocho": {
		"row": 0,
		"bigs": ["Kyle Samonte"],
		"littles": ["Marcus Mata", "Nicholas Te"],
		# "littles": [],
		"x": 0,
		"y": 0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"animated": False,
		"top_big": False,
	},
	"Adrian Marc Santiago": {
		"row": 0,
		"bigs": [],
		"littles" : ['Ryan Lo'],
		"x": 0,
		"y": 0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"animated": False,
		"top_big": False,
	},
	"Sam Solomon": {
		"row": 0,
		"bigs": [],
		"littles" : ['Joshua Sixto Beltran'],
		"x": 0,
		"y": 0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"animated": False,
		"top_big": False,
	},
	"Daniel Jose": {
		"row": 0,
		"bigs": ['big 1', 'big 2'],
		# "bigs": [],
		# "littles": ["Christian Chow"],
		"littles": ["Christian Chow"],
		"x": 0,
		"y": 0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"animated": False,
		"top_big": False,
	},
	"Christian Chow": {
		"row": 0,
		"bigs": ["Kyle Samonte","Daniel Jose",],
		"littles": ["Jordan Wong", "John Brooks"],
		# "littles": [],
		"x": 0,
		"y": 0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"animated": False,
		"top_big": False,
	},
	"Nicholas Te": {
		"row": 0,
		"bigs": ["Alessandro Bischocho", "lil 2"],
		"littles": [],
		"x": 0,
		"y": 0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"animated": False,
		"top_big": False,
	},
	"Marcus Mata": {
		"row": 0,
		"bigs": ['Alessandro Bischocho', "lil 2"],
		"littles": [],
		"x": 0,
		"y": 0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"animated": False,
		"top_big": False,
	},
	"Jordan Wong": {
		"row": 0,
		"bigs": ['Christian Chow', 'Shane Casey'],
		"littles": [],
		"x": 0,
		"y": 0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"animated": False,
		"top_big": False,
	},
	"Shane Casey": {
		"row": 0,
		"bigs": [],
		"littles" : ['Jordan Wong'],
		"x": 0,
		"y": 0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"animated": False,
		"top_big": False,
	},
	"John Brooks": {
		"row": 0,
		"bigs": ['Christian Chow'],
		"littles": ['lil 1'],
		"x": 0,
		"y": 0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"animated": False,
		"top_big": False,
	},
	"lil 1": {
		"row": 0,
		# "bigs": ['big 1', 'big 2'],
		"bigs": ["John Brooks", "big 3"],
		"littles" : [],
		"x": 0,
		"y": 0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"animated": False,
		"top_big": False,
	},
	"lil 2": {
		"row": 0,
		"bigs": ['big 3'],
		"littles": ["Marcus Mata", "Nicholas Te"],
		# "littles" : [],
		"x": 0,
		"y": 0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"animated": False,
		"top_big": False,
	},
	"lil 3": {
		"row": 0,
		"bigs": ['big 1', 'Ryan Lo'],
		"littles" : [],
		"x": 0,
		"y": 0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"animated": False,
		"top_big": False,
	},
	"big 1": {
		"row": 0,
		"bigs": ['big 5'],
		"littles" : ['lil 3','Daniel Jose'],
		"x": 0,
		"y": 0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"animated": False,
		"top_big": False,
	},
	"big 2": {
		"row": 0,
		"bigs": [],
		"littles" : ['Daniel Jose'],
		"x": 0,
		"y": 0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"animated": False,
		"top_big": False,
	},
	"big 3": {
		"row": 0,
		"bigs": [],
		"littles": ['Kyle Samonte', 'lil 3', 'lil 2', 'lil 1'],
		# "littles": ['Kyle Samonte'], 
		"x": 0,
		"y": 0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"animated": False,
		"top_big": False,
	},
	"big 4": {
		"row": 0,
		"bigs": [],
		"littles" : ['Kyle Samonte', 'Daniel Jose'],
		"x": 0,
		"y": 0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"animated": False,
		"top_big": False,
	},
	"big 5": {
		"row": 0,
		"bigs": [],
		"littles" : ['big 1'],
		"x": 0,
		"y": 0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"animated": False,
		"top_big": False,
	}
}
test2 = {
	"Elliot Bernardo": {
		"row": 0,
		"bigs": ['Gabby Arceo', 'Matthew Beltran'],
		"littles": [],	
		"x":0,
		"y":0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"top_big": False,
	}, 	
	"Emily Ramos": {
		"row": 0,
		"bigs": ['Gabby Arceo'],
		"littles": ["lil 1","lil 2", "lil 3"],	
		"x":0,
		"y":0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"top_big": False,
	}, 	
	"Gabby Arceo": {
		"row": 0,
		"bigs": ['Adrian Marc Santiago', 'MJ Salanga'],
		"littles": ['Elliot Bernardo', 'Emily Ramos'],	
		"x":0,
		"y":0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"top_big": False,
	}, 	
	"Matthew Beltran": {
		"row": 0,
		"bigs": ['Adrian Marc Santiago', 'MJ Salanga'],
		"littles": ['Elliot Bernardo', 'Gabriel Gutierrez'],	
		"x":0,
		"y":0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"top_big": False,
	},
	"Gabriel Gutierrez": {
		"row": 0,
		"bigs": ['Matthew Beltran'],
		"littles": [],	
		"x":0,
		"y":0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"top_big": False,
	}, 	
	"Adrian Marc Santiago": {
		"row": 0,
		"bigs": [],
		"littles": ['Gabby Arceo', 'Matthew Beltran'],	
		"x":0,
		"y":0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"top_big": False,
	}, 	
	"MJ Salanga": {
		"row": 0,
		"bigs": [],
		"littles": ['Gabby Arceo', 'Matthew Beltran'],	
		"x":0,
		"y":0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"top_big": False,
	},
	"lil 1": {
		"row": 0,
		"bigs": ["Emily Ramos"],
		"littles": [],	
		"x":0,
		"y":0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"top_big": False,
	},
	"lil 2": {
		"row": 0,
		"bigs": ["Emily Ramos"],
		"littles": [],	
		"x":0,
		"y":0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"top_big": False,
	},
	"lil 3": {
		"row": 0,
		"bigs": ["Emily Ramos"],
		"littles": ["lil 4", "lil 5"],	
		"x":0,
		"y":0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"top_big": False,
	},
	"lil 4": {
		"row": 0,
		"bigs": ["lil 3"],
		"littles": [],	
		"x":0,
		"y":0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"top_big": False,
	},
	"lil 5": {
		"row": 0,
		"bigs": ["lil 3"],
		"littles": [],	
		"x":0,
		"y":0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"top_big": False,
	},
}

# Constants
MAX_QUEUE_SIZE = 100
# colors
DEFAULT_COLOR = "orange"
GHOST_PARENT_COLOR = "#93e0f5"
NORMAL_GHOST_COLOR = "#f56262"
# opacities
GHOST_TEXT_OPACITY = 0.9
GHOST_RECT_OPACITY = 0.6
GHOST_LINE_OPACITY = 0.7

x_increments = 100 # tentative?
y_increments = 100 # ?

# Global variables to be used for animations (set in draw_f).
main_root = None

import animation
import svgnodes

from collections import deque

# Draws the subtree of the root given in the tree
#	Parameters:
# 		tree {Hash Map / Dict} - Has all the information about people in our tree
# 		person {String} - name of the person we are processing
#		excluding { "" | String} - person to exclude from drawing of subtree.
#		color {String | HEX Color} - color that (person)'s node will be drawn with
#	Notes:
#		This is a recursive function that operates in postorder.
#		This function does not draw the ghost parents first (person) in the recursive call
#		This function (at its current form) does not place (person)'s node in the direct middle of the subtree.
#	ASSUMPTION: 
# 		- Ghost child nodes are ALWAYS placed to the RIGHT of real child nodes.
# 	Returns the farthest right node in the subtree.
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

	my_starting_x = tree[person]["x"]

	# Give initial x and y positions to littles if they are NOT visited and create their parent ghost nodes
	x_inc = 0
	for little in unvisited_littles:
		tree[little]["x"] = tree[person]["x"] + x_inc * x_increments
		tree[little]["y"] = tree[person]["y"] + 2 * y_increments
		x_inc += 1
		# Check if littles have bigs that are not (person); if they do, make parent ghost nodes
		if(len(tree[little]["bigs"]) > 1):
			start_x = tree[little]["x"]
			ghost_x_inc = 0
			for big in tree[little]['bigs']:
				if(big != person):
					new_ghost_node = {
						"name": big,
						"my_node": svgnodes.make_node(big, GHOST_PARENT_COLOR, GHOST_RECT_OPACITY),
						"x": tree[little]["x"] + (ghost_x_inc * x_increments),
						"y": tree[little]["y"] - 1 * y_increments, 
					}
					add_ghost_mouseover_event(tree, little, new_ghost_node)
					add_click_event(tree, person=little, ghost_dict=new_ghost_node)
					tree[little]["parent_ghost_nodes"].append(new_ghost_node)
					svgnodes.set_node_position(new_ghost_node["my_node"], new_ghost_node["x"], new_ghost_node["y"])
					ghost_x_inc += 1

	# If the littles ARE visited, it means they are somewhere else in the tree. make a child ghost node instead
	for little in visited_littles:
		new_ghost_node = {
			"name": little,
			"my_node": svgnodes.make_node(little, NORMAL_GHOST_COLOR, GHOST_RECT_OPACITY),
			"x": tree[person]["x"] + x_inc * x_increments,
			"y": tree[person]["y"] + 2 * y_increments, 
		}
		x_inc += 1 # treat it like a real node for far_right_x
		add_ghost_mouseover_event(tree, person, new_ghost_node)
		add_click_event(tree, person=person, ghost_dict=new_ghost_node)
		tree[person]["child_ghost_nodes"].append(new_ghost_node)
		svgnodes.set_node_position(new_ghost_node["my_node"], new_ghost_node["x"], new_ghost_node["y"])
		print("hey")
	total_length = unvisited_lils_length + len(visited_littles)

	# If we have 1 or no little, skip most of the alignment stuff
	if(total_length <= 1):
		far_right_x = tree[person]["x"]

		# Draw little if they have one
		if(unvisited_lils_length == 1):
			# draw_tree_down can move the little's node, so move (person)'s node equal to the distance travelled by little's node
			start_x = tree[unvisited_littles[0]]["x"]
			far_right_x = draw_tree_down(tree, unvisited_littles[0], excluding)
			end_x = tree[unvisited_littles[0]]["x"]
			distance_travelled = end_x - start_x
			tree[person]["x"] += distance_travelled

		# Move ghost nodes above (person)'s node if (person) moved at all.
		if(len(tree[person]["parent_ghost_nodes"]) > 0):
			ghost_x_inc = 0
			start_x = tree[person]["x"]
			for ghost in tree[person]["parent_ghost_nodes"]:
				ghost["x"] = start_x + ghost_x_inc * x_increments
				svgnodes.set_node_position(ghost["my_node"], ghost["x"], ghost["y"])
				ghost_x_inc += 1
			distance_between_ghosts = (ghost_x_inc - 1) * x_increments 
			if(start_x + distance_between_ghosts > far_right_x):
				far_right_x = start_x + distance_between_ghosts 
			offset = distance_between_ghosts / 2
			tree[person]["x"] += offset
			offset_littles_x(tree, person, offset)

		svgnodes.update_node_position(tree, person)
		return far_right_x

	# -------------- if (person) has more than 1 little ----------------
	# Find current far_right_x, checking through both real and ghost child nodes
	#	- Does not check parent ghost nodes because they are misplaced at the moment
	# print(f"{person} is looking for far_right_x. unv_length: {unvisited_lils_length}")
	my_far_right_x = 0

	# If a ghost is a far left child, there are no real children
	if unvisited_lils_length > 1:
		my_far_right_x = tree[ unvisited_littles[-1] ]["x"]
	if len(visited_littles) > 0:
		my_far_right_x = tree[person]["child_ghost_nodes"][-1]["x"]

	# Move person to the middle of its child nodes BEFORE drawing their subtree.
	tree[person]["x"] = (my_starting_x + my_far_right_x) / 2

	farthest_right_x = my_far_right_x
	# Draw subtrees of littles.
	your_far_right_x = 0
	for lil in unvisited_littles:
		start_x = tree[lil]["x"]
		your_far_right_x = draw_tree_down(tree, lil, excluding)
		# Update farthest_right_x
		if(farthest_right_x < your_far_right_x):
			farthest_right_x = your_far_right_x
		# If person moved from little's draw_tree_down, we must offset all right sibs using (person)'s "littles" list.
		if(your_far_right_x != start_x):
			temp_far_right_x = shift_right_sibs(tree, unvisited_littles, lil, shared_big=person, left_boundary=your_far_right_x)
			if(temp_far_right_x > farthest_right_x):
				farthest_right_x = temp_far_right_x

	# Center (person) over their littles and ghost littles
	left_bound = None
	right_bound = None
	if unvisited_lils_length > 0:
		left_bound = tree[ unvisited_littles[0] ]["x"]
	else:
		left_bound = tree[person]["child_ghost_nodes"][0]["x"]
	
	if unvisited_lils_length > 1:
		right_bound = tree[ unvisited_littles[-1] ]["x"]
	if len(visited_littles) > 0:
		right_bound = tree[person]["child_ghost_nodes"][-1]["x"]
	
	tree[person]["x"] = (left_bound + right_bound) / 2

	# Move (person)'s parent ghost nodes and move (person) between ghost nodes if there is more than 1
	if(len(tree[person]["parent_ghost_nodes"]) > 0):
		ghost_x_inc = 0
		start_x = tree[person]["x"]
		for ghost in tree[person]["parent_ghost_nodes"]:
			ghost["x"] = tree[person]["x"] + ghost_x_inc * x_increments
			svgnodes.set_node_position(ghost["my_node"], ghost["x"], ghost["y"])
			ghost_x_inc += 1

		distance_between_ghosts = (ghost_x_inc - 1) * x_increments 
		tree[person]["x"] += distance_between_ghosts / 2
		# this will only run if (person) has like 5 bigs and 2 lils w/o thier own lils.
		if(start_x + distance_between_ghosts > farthest_right_x):
			farthest_right_x = start_x + distance_between_ghosts 
	
	# Update (person)'s node
	svgnodes.update_node_position(tree, person)
	# print(f"{person} is done and returning furthest_right of {farthest_right_x}")
	return farthest_right_x

# Offsets right sibs and their children using either a boundary or set amount. Used only in draw_tree_down atm
#	Parameters:
# 		tree {Hash Map / Dict} - Has all the information about people in our tree
#		sibs_list {String list} - Has list of sibs in order. IT MUST CONTAIN (person)  
# 		person {String} - name of the person we are processing
#		shared_big {String} - name of big that the sibs are being read from.
#		x_amount {Number | 0} - amount used for offsetting nodes. NOT USED atm
#		left_boundary {Number | None} - The boundary which all nodes must be to the right of.
#	ASSUMPTION:
#		Ghost child nodes are ALWAYS placed to the RIGHT of real child nodes.
# Returns the far_right_x of all nodes
def shift_right_sibs(tree, sibs_list, person, shared_big, x_amount = 0, left_boundary = None):
	farthest_right_x = tree[person]["x"]
	
	# Find the index of (person)
	sibs_length = len(sibs_list)
	sib = sibs_list.index(person) + 1

	# Find the distance that will be applied to all right sibs.
	# Formula is |first_right_sib_x - left_boundary| + (1 * x_increments) + x_amount
	sib_dict = None
	if(left_boundary == None):
		travel_distance = x_amount
	# If we have no real sibs but some ghost sibs
	elif(sib == sibs_length and len(tree[shared_big]["child_ghost_nodes"]) > 0):
		travel_distance = abs(tree[shared_big]["child_ghost_nodes"][0]["x"] - left_boundary) + (1 * x_increments) + x_amount
	# If we have no right sibs
	elif(sib == sibs_length):
		return farthest_right_x
	else:
		sib_dict = tree[sibs_list[sib]]
		travel_distance = abs(sib_dict["x"] - left_boundary) + (1 * x_increments) + x_amount

	# Offset ghost sibs using the shared_big
	for ghost in tree[shared_big]["child_ghost_nodes"]:
		ghost["x"] += travel_distance
		if(ghost["x"] > farthest_right_x):
			farthest_right_x = ghost["x"]
		svgnodes.set_node_position(ghost["my_node"], ghost["x"], ghost["y"])

	# If there are no real right sibs, return now!
	if(sib_dict == None):
		return farthest_right_x

	# Offset all real right sibs
	while(sib < sibs_length):
		sib_dict = tree[sibs_list[sib]]
		# Move sib
		sib_dict["x"] += travel_distance
		# Move sib's ghost parents
		for ghost in sib_dict["parent_ghost_nodes"]:
			ghost["x"] += travel_distance
			svgnodes.set_node_position(ghost["my_node"], ghost["x"], ghost["y"])
		# move sib's ghost children
		for ghost in sib_dict["child_ghost_nodes"]:	
			ghost["x"] += travel_distance	
			svgnodes.set_node_position(ghost["my_node"], ghost["x"], ghost["y"])
		# move sib's visited children
		if(sib_dict["visited"] and len(tree[sibs_list[sib]]["littles"]) > 0):
			offset_littles_x(tree, sibs_list[sib], travel_distance)
		sib += 1
	return farthest_right_x

# Offsets right sibs and their children using either a boundary or set amount. Used only in draw_tree_down atm
#	Parameters:
# 		tree {Hash Map / Dict} - Has all the information about people in our tree
# 		person {String} - name of the person we are processing
#		amt {Number | 0} - amount used for offsetting nodes.
#		not_including {String | ""} - name of little to not offset. used mainly when drawing tree upwards
# Returns the farthest_right_x of the nodes operated on.
def offset_littles_x(tree, person, amt, not_including=""):
	farthest_right_x = tree[person]["x"]

	# If we find more people that we don't want to include, add them to a list.
	skip_list = []
	skip_list.append(not_including)

	# Update person's ghost children and add them to skip_list
	for ghost in tree[person]["child_ghost_nodes"]:
		ghost["x"] += amt
		if(ghost["x"] > farthest_right_x):
			farthest_right_x = ghost["x"]	
		# Don't update the actual node of ghost child.
		svgnodes.set_node_position(ghost["my_node"], ghost["x"], ghost["y"])
		skip_list.append(ghost["name"])

	# Offset each person’s x in the list by (amt)
	for little in tree[person]["littles"]:
		# Avoid anyone in skip_list
		skip = False
		for skipped in skip_list:
			if(little == skipped):
				skip = True
		# If we are using only_include and little is not them, skip. This is spaghetti code btw
		if(not tree[little]["visited"] or skip): 
			continue
		# Offset little
		tree[little]["x"] += amt
		if(tree[little]["x"] > farthest_right_x):
			farthest_right_x = tree[little]["x"]
		svgnodes.set_node_position(tree[little]["my_node"], tree[little]["x"], tree[little]["y"])

		# Update little's ghost parents
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
#		queue {collections.deque} - Holds data of what to operate on next. BFS algorithm.
# 		direction {-1 | +1} - Direction of drawing, either left or right
#		outward_offset {Number} - Offset generated from the previous iteration of BFS.
#		excluding {list} - who we should exclude from drawing.
# Notes:
#		- IMPORTANT nodes are created from their littles' function, so they are NOT created during thier function.
#
#		- Queue operations are append() to add and popleft() do remove.
#		- Queue has data of [current_person, who_they_came_from]
#
#		- "top_big" attribute means they are a part of the "fanning" pattern at the top of the tree.
def draw_tree_up(tree, queue, direction, outward_offset, excluding = []):
	front = queue.popleft()
	person = front[0]
	current_little = front[1]

	tree[person]["x"] += outward_offset
	# Draw the subtree
	starting_x = tree[person]["x"]
	far_x = draw_tree_down(tree, person, excluding=current_little)
	tree[person]["top_big"] = True

	# If we are moving left, offset all nodes to the left by the distance travelled.
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
			}
			add_ghost_mouseover_event(tree, person, new_ghost_node)
			add_click_event(tree, person=person, ghost_dict=new_ghost_node)
			tree[big]["parent_ghost_nodes"].append(new_ghost_node)
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
# Parameters are self-explanitory
# NOTE 	The reason why we make immediate parent nodes here is because during 
# 		the draw_tree_up, we want a more balanced tree. If we didn't visit
#		the node here and the immediate right parents are found in the left
# 		parent's tree (2 bigs pick up 2 littles case), it would be extremely
#		unbalanced. Can be removed if we improve BFS by alternating directions.
# NOTE Queues have data of [current_person, who_they_came_from]
def draw_full_tree(tree, person):
	# draw_lines(20) # debug; can comment out.
	# Make root node.
	tree[person]["visited"] = True
	tree[person]["x"] = 0
	tree[person]["y"] = 0
	html_node = svgnodes.make_node(person, "#b869f0")
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
	tree[person]["x"] = (ending_x + starting_x) / 2 # corner cut right here. could be centered between immediate children instead of whole tree.
	svgnodes.update_node_position(tree, person)

	bigs_length = len(tree[person]["bigs"])
	if(bigs_length == 0):
		# no bigs, no problems
		return
	
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
			tree[big]["top_big"] = True
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
		tree[person]["top_big"] = True
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
			tree[big]["top_big"] = True
			html_node = svgnodes.make_node(big, DEFAULT_COLOR)
			svgnodes.set_node_position(html_node, tree[big]["x"], tree[big]["y"])
			tree[big]["my_node"] = html_node
			add_real_mouseover_event(tree, big)
			add_click_event(tree, person=big)

			# Append to Queue
			leftQueue.append([big, person])
			bigIndex -= 1

		# Add right bigs to queue
		bigIndex = middle_index
		while bigIndex < bigs_length:
			big = tree[person]["bigs"][bigIndex]

			# Give position
			tree[big]["y"] = tree[person]["y"] - (2 * y_increments)

			# Make node
			tree[big]["visited"] = True
			tree[big]["top_big"] = True
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


# Gives mouseover behavior to (person)'s node
def add_real_mouseover_event(tree, person):
	print(f"mouseover: {person}")
	tree[person]["my_node"][1].addEventListener("mouseover", lambda e: animation.real_mouseover_event(e, tree, person))

# Gives mouseover behavior to (ghost_dict)'s node
def add_ghost_mouseover_event(tree, real_person, ghost_dict):
	ghost_dict["my_node"][1].addEventListener("mouseover", lambda e: animation.ghost_mouseover_event(e, tree, real_person, ghost_dict))

# Gives click behavior to either person or ghost
def add_click_event(tree, person=None, ghost_dict=None):
	if(ghost_dict == None):
		tree[person]["my_node"][1].addEventListener("click", lambda e: click_event(e, tree, person=person))
	else:
		ghost_dict["my_node"][1].addEventListener("click", lambda e: click_event(e, tree, person=person, ghost_dict=ghost_dict))

# On a click, make a new tree with clicked person as the root.
def click_event(e, tree, person=None, ghost_dict=None):
	animation.resetAnimations()
	svgnodes.removeNodes()
	resetDict(tree)
	if(ghost_dict == None):
		draw_full_tree(tree, person) # NEEDS TO HAVE TREE OF PERSON CLICKED AVAILABLE
	else:
		draw_full_tree(tree, ghost_dict["name"])

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

test4 = {
	"big 1": {
		"row": 0,
		"bigs": ["big 3"],
		"littles": ['lil 1', 'lil 2', 'lil 3'],	
		"x":0,
		"y":0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"top_big": False,
		"lines": []
	}, 	
	"lil 1": {
		"row": 0,
		"bigs": ["big 1", "big 2"],
		"littles": ["lil 1 1", "lil 1 2"],	
		"x":0,
		"y":0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"top_big": False,
		"lines": []
	}, 
	"lil 2": {
		"row": 0,
		"bigs": ["big 1"],
		"littles": [],	
		"x":0,
		"y":0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"top_big": False,
		"lines": []
	}, 	
	"lil 3": {
		"row": 0,
		"bigs": ["big 1"],
		"littles": [],	
		"x":0,
		"y":0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"top_big": False,
		"lines": []
	}, 
	"big 2": {
		"row": 0,
		"bigs": [],
		"littles": ["lil 1"],	
		"x":0,
		"y":0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"top_big": False,
		"lines": []
	}, 
	"big 3": {
		"row": 0,
		"bigs": [],
		"littles": ["big 1"],	
		"x":0,
		"y":0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"top_big": False,
		"lines": []
	}, 
	"lil 1 1": {
		"row": 0,
		"bigs": ["lil 1"],
		"littles": [],	
		"x":0,
		"y":0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"top_big": False,
		"lines": []
	}, 	
	"lil 1 2": {
		"row": 0,
		"bigs": ["lil 1"],
		"littles": [],	
		"x":0,
		"y":0,
		"visited": False,
		"parent_ghost_nodes": [],
		"child_ghost_nodes": [],
		"top_big": False,
		"lines": []
	}, 
}

# draw_full_tree(test4, "lil 1")
# draw_lines(test4, "lil 1")

# def addAnimation(elem, OG_y):
# 	animation = document.createElementNS('http://www.w3.org/2000/svg', 'animate'); 
# 	animation.setAttribute('attributeName', "y")
# 	animation.setAttribute('dur', "0.05s")
# 	animation.setAttribute('from', f"{OG_y-NODE_HEIGHT/2}")
# 	animation.setAttribute('to', f'{OG_y-NODE_HEIGHT/2-2}')
# 	animation.setAttribute('fill', 'freeze')
# 	elem.appendChild(animation)
# 	animation.beginElement()
# 	return animation