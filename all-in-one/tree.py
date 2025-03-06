# Treeclass This code makes the edge list used for drawing the tree.
# import app

# App: This file gets the data from the backend
from pyscript import when, fetch, document, window
import asyncio
import json
from collections import deque


# Constants
NODE_WIDTH = 75
NODE_HEIGHT = 50
STROKE_WIDTH = 2

CHILD_LINE_COLOR = "black"
REAL_PARENT_LINE_COLOR = "blue"
GHOST_PARENT_LINE_COLOR = "green"

REAL_LINE_CONNECT_COLOR = "red"

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

MAX_QUEUE_SIZE = 100
REAL_LINE_CONNECT_COLOR = "red"
ANIMATED_GHOST_RECT_OPACITY = 0.9

# Global variables to be used for animations.
info_box = None
animated = deque([], MAX_QUEUE_SIZE)
# Global Variable used throughout code
main_root = None
# Global Variables for autocomplete logic
item_box = None
values = []


# app.data is originally set to None
#   app.py module runs asynchronously, and the #testButton will become visible when
#   data is loaded, so no need to worry about app.data = NONE unless server shuts down

# Function that splits the names gathered from database into separate strings.
def splitComma(input): 
  if input == None or input == "": # in case there is nothing in input
    return []
  arr = input.split(",")
  # if there is only one person, no need to .strip()
  if len(arr) == 1:
    return arr
  newArr = []
  for elt in arr:
    newArr.append(elt.strip())
  return newArr

# Function that returns the row number of the name requested
def searchNameForIndex(name):
    input = name.strip()
    out = binarySearch(data, 0, len(data) - 1, input.lower()) 
    return out
      
# Binary search that compares the first elements of each row.
# .lower() is used for string comparison (should use casefold() but micropython doesn't support that cmd)
def binarySearch(values, lo, hi, target):
    if lo <= hi:
        mid = (hi + lo) // 2
        temp = data[mid][0].strip().lower()
        if(temp == target):
            return mid
        if target > temp: # search right
            return binarySearch(values, mid + 1, hi, target)
        if target < temp: # search left
            return binarySearch(values, lo, mid - 1, target)
    return -1 # nada

# Class that holds tree data
class Tree:
  def __init__(self, input):
    # Optimization: If our inputted name is already in tree, that means all their
    # relatives are in the tree, so we don't need to make a new tree.
    self.in_tree = False
    for row in data:
       if(row[0].lower() == input.lower()):
          self.in_tree = True
          self.root = row[0] # name of person we want to build tree for
          break
    if(self.in_tree):
      self.dict = {} # used to store the edge list
    return
    
  
  # Recursive function to build the dictionary with all necessary nodes
  # Could be optimized to only look for necessary nodes for our tree.
  # Parameters:
  #   input {String} - Name of the person currently being operated on.
  # Each attribute:
  #   row: row # of (input)
  #   x: x-position in SVG
  #   y: y-position in SVG
  #   visited: Tells if (input)'s node has been created yet or not.
  #   parent_ghost_nodes: list that stores parent_ghost_nodes.
  #   child_ghost_nodes: list that stores child_ghost_nodes.
  #   top_big: tells if (input) is a top_big or not (see draw.draw_full_tree())
  #   my_node: Stores the data for the SVG (nodes are lists of [rectangle, text])
  #   lines: Stores the lines that should be highlighted when (input) is being animated.
  def makeTree(self, input):

    # process data for (input)
    row = searchNameForIndex(input)
    if(row == -1):
      print(f"treeclass: did not find {input}")
      return
    # print(f"  row: {row}")
    self.dict[input] = {}
    self.dict[input]["row"] = row
    self.dict[input]["x"] = 0
    self.dict[input]["y"] = 0
    self.dict[input]["visited"] = False
    self.dict[input]["parent_ghost_nodes"] = []
    self.dict[input]["child_ghost_nodes"] = []
    self.dict[input]["top_big"] = False
    self.dict[input]["my_node"] = None
    self.dict[input]["lines"] = []
    # Set bigs array
    if(len(data[row]) < 3):
      self.dict[input]["bigs"] = []
    else:
      self.dict[input]["bigs"] = splitComma(data[row][2])
    # Set littles array
    if(len(data[row]) < 2):
      self.dict[input]["littles"] = []
    else:
      self.dict[input]["littles"] = splitComma(data[row][1])

    # If (input)'s bigs or littles have not been processed yet, process them.
    for bigName in self.dict[input]["bigs"]:
      if(bigName not in self.dict):
        self.makeTree(bigName)
    for lilName in self.dict[input]["littles"]:
      if(lilName not in self.dict):
        self.makeTree(lilName)

  # Function to print data of all nodes in the tree
  def printTree(self):
      for person in self.dict:
          print(person)
          print("  row#: " + str(self.dict[person]["row"]))
          print("  bigs: " + str(self.dict[person]["bigs"]))
          print("  lils: " + str(self.dict[person]["littles"]))
      return

# Pyscript syntax for setting a click listener on button with id = "testButton"
@when("click", "#testButton")
def createTreeOnPage():
  print("Button Pushed.")
  global input_name
  input_name = document.getElementById("tree_name").value
  if(data == None):
    print(f"Data not recieved yet. Aborting...")
    return
  tree = Tree(input_name) # tests code. output found in console
  if(not tree.in_tree):
     print("Person is not in tree.")
     return
  tree.makeTree(tree.root)
  click_event(None, tree.dict, person=tree.root)
#   set_tree(None, tree.dict, person=tree.root)
  return

# app.py

# NOTE: we can use web-workers to take a load off the main page but pyscript doesn't
#		play nicely with web-workers. 
#		if we use web-workers later down the line, there will be a problem using the 
#		DOM. This is because there are necessary headers and config settings that
#		make the DOM not work with web workers.

# TODO GET_URL could be an environment varible
GET_URL = "https://python-sheets-data-gixw5eexra-uw.a.run.app"
# GET_URL = "https://jsonplaceholder.typicode.com/users"

data = None
# This variable used to store data from the API
# NOTE: in the data returned, anything in the last column will be omitted if there is no value 
# 		(for us, if the person has no bigs, their row will only have 2 indexes instead of 3).
#		to address this, code has been put in treeclass.splitComma() that addresses this.

# Getter functions of data (not used atm)
def getAllData():
	return data
def getData(row, col):
	if(0 <= row and row < len(data) and 0 <= col and col < len(data[0])):
		return data[row][col]
	return None

# Function that makes the request to the API
# 	Status code is 200 if the request was sucessful
async def getAPIData():
	rawResult = None
	try:
		rawResult = await fetch(
			url=GET_URL, 
			method="GET",
			headers={"Content-Type": "application/json; charset=UTF-8"}
		)
		result = await rawResult.text()
		global data
		data = json.loads(result)["data"] # the extra ["data"] is here because of the way the json is formatted
		data.pop(0) # removes the column names from the data
		return
	except:
		print(f"app.py: Something went wrong (ERRNO {rawResult.status}).")
		return

# Edit the DOM after data is retrieved
async def main():
	await getAPIData()
	document.getElementById("load-screen").style.display = "none"
	document.getElementById("testButton").style.display = "inline"
	prepare_svg()
	return

# necessary to run async code on browser.
def getData(event):
	asyncio.create_task(main())

# Run the async code as soon as all our modules are loaded
window.addEventListener("py:all-done", getData)

# Takes two arguments, input element and array of strings
def set_autocomplete(input):
	input_field = document.getElementById("tree_name")
	global values
	for row in data:
		values.append(row[0])
	input.addEventListener("input", lambda e: inputEvent(input_field))

def inputEvent(input):
	clear_autocomplete()
	global item_box
	value = input.value
	value_length = len(value)
	container = document.getElementById("autocomplete-container")
	item_box = document.createElement("DIV")
	item_box.setAttribute("id", "autocomplete-box")
	document.body.addEventListener("click", clear_autocomplete)
	container.appendChild(item_box)
	global values
	for person in values:
		if(person.strip().lower()[0:value_length] == value.lower()):
			new_option = document.createElement("DIV")
			new_option.setAttribute("class", "autocomplete-item")
			new_option.innerHTML = person
			new_option.addEventListener("click", lambda e: click_option(e))
			item_box.appendChild(new_option)

def click_option(event):
	if(event != None):
		name = event.target.innerHTML
		print(name)
		document.getElementById("tree_name").value = name
		clear_autocomplete()

def clear_autocomplete(e=None):
	document.body.removeEventListener("click", clear_autocomplete)
	item_box = document.getElementById("autocomplete-box")
	if(item_box != None):
		while(item_box.firstChild):
			item_box.removeChild(item_box.lastChild)
		item_box.parentNode.removeChild(item_box)


# Draw.py

# Draws the subtree of the root given in the tree
#	Parameters:
# 		tree {Hash Map / Dict} - Has all the information about people in our tree
# 		person {String} - name of the person we are processing
#		excluding { "" | String} - person to exclude from drawing of subtree.
#		color {String | HEX Color} - color that (person)'s node will be drawn with
#	Notes:
#		This is a recursive function that operates in preorder.
#		This function does not draw the ghost parents first (person) in the recursive call
#	ASSUMPTION: 
# 		- Ghost child nodes are ALWAYS placed to the RIGHT of real child nodes.
# 	Returns the position of the farthest right node in the subtree.
def draw_tree_down(tree, person, excluding="", color=DEFAULT_COLOR):
	# Create node if it has not already been created and store it in (html_node)
	html_node = None
	if(tree[person]["visited"] == False):
		tree[person]["visited"] = True
		html_node = make_node(person, color)
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


	# If we have no littles, skip most of the alignment stuff
	total_length = unvisited_lils_length + len(visited_littles)
	if(total_length == 0):
		update_node_position(tree, person)
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
						"my_node": make_node(big, GHOST_PARENT_COLOR, GHOST_RECT_OPACITY),
						"x": tree[little]["x"] + (ghost_x_inc * x_increments),
						"y": tree[little]["y"] - 1 * y_increments, 
						"lines": []
					}
					add_ghost_mouseover_event(tree, little, new_ghost_node)
					add_click_event(tree, person=little, ghost_dict=new_ghost_node)
					tree[little]["parent_ghost_nodes"].append(new_ghost_node)
					set_node_position(new_ghost_node["my_node"], new_ghost_node["x"], new_ghost_node["y"])
					ghost_x_inc += 1
			# If we had more than one ghost big, make sure to center (person) and their children under the nodes.
			if(ghost_x_inc > 1):
				distance_between_ghosts = (ghost_x_inc - 1) * x_increments 
				begin_x += distance_between_ghosts
				offset = distance_between_ghosts / 2
				tree[little]["x"] += offset
				offset_littles_x(tree, little, offset)
				update_node_position(tree, little)
		lil_index += 1

	# If the littles ARE visited, it means they are somewhere else in the tree. Make a child ghost node instead at the far right of the subtree.
	for little in visited_littles:
		new_ghost_node = {
			"name": little,
			"my_node": make_node(little, NORMAL_GHOST_COLOR, GHOST_RECT_OPACITY),
			"x": begin_x,
			"y": tree[person]["y"] + 2 * y_increments, 
			"lines": []
		}
		add_ghost_mouseover_event(tree, person, new_ghost_node)
		add_click_event(tree, person=person, ghost_dict=new_ghost_node)
		tree[person]["child_ghost_nodes"].append(new_ghost_node)
		set_node_position(new_ghost_node["my_node"], new_ghost_node["x"], new_ghost_node["y"])
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

	update_node_position(tree, person)

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
		set_node_position(ghost["my_node"], ghost["x"], ghost["y"])
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
		set_node_position(tree[little]["my_node"], tree[little]["x"], tree[little]["y"])

		# Update (little)'s ghost parents
		for ghost in tree[little]["parent_ghost_nodes"]:
			ghost["x"] += amt
			set_node_position(ghost["my_node"], ghost["x"], ghost["y"])

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
#		- IMPORTANT nodes are created from their littles' function, so they are NOT created during thier function.
#		- Queue operations are append() to add and popleft() to remove.
#		- Queue has data of [current_person, who_they_came_from]
#		- "top_big" attribute means they are a part of the "fanning" pattern at the top of the tree.
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
			# WARNING: extremely scuffed "centering" being done here. Will make the tree look weirder the more bigs are attatched to one person.
			# Works ok with someone with 2 parent_ghost_nodes, but the more the worse it gets.
			while(ghost_index < num_ghosts):
				ghost_dict = tree[person]["parent_ghost_nodes"][ghost_index]
				ghost_dict["x"] -= 0.5 * x_increments
				set_node_position(ghost_dict["my_node"], ghost_dict["x"], ghost_dict["y"])
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
			"my_node": make_node(person, NORMAL_GHOST_COLOR, GHOST_RECT_OPACITY),
			"x": your_x,
			"y": tree[current_little]["y"] - 1 * y_increments, 
			"lines": []
		}
		add_ghost_mouseover_event(tree, current_little, new_ghost_node)
		add_click_event(tree, person=current_little, ghost_dict=new_ghost_node)
		tree[current_little]["parent_ghost_nodes"].append(new_ghost_node)
		set_node_position(new_ghost_node["my_node"], new_ghost_node["x"], new_ghost_node["y"])
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
	update_node_position(tree, person)

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
				"my_node": make_node(big, NORMAL_GHOST_COLOR, GHOST_RECT_OPACITY),
				"x": tree[person]["x"] + (ghost_x_inc * x_increments * direction),
				"y": tree[person]["y"] - 1 * y_increments, 
				"lines": []
			}
			add_ghost_mouseover_event(tree, person, new_ghost_node)
			add_click_event(tree, person=person, ghost_dict=new_ghost_node)
			tree[person]["parent_ghost_nodes"].append(new_ghost_node)
			set_node_position(new_ghost_node["my_node"], new_ghost_node["x"], new_ghost_node["y"])
			ghost_x_inc += 1
		bigIndex += direction

	# If there were more than 1 ghost bigs, offset (person) and thier littles
	if ghost_x_inc > 0:
		ghost_offset = (ghost_x_inc - 1) * x_increments / 2 * direction
		tree[person]["x"] += ghost_offset
		update_node_position(tree, person)
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
	# Make root node.
	tree[person]["visited"] = True
	tree[person]["x"] = 0
	tree[person]["y"] = 0
	html_node = make_node(person, f"{ROOT_COLOR}")
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
	# tree[person]["x"] = (ending_x + starting_x) / 2 # corner cut right here. could be centered between immediate children instead of whole tree.
	update_node_position(tree, person)

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
			html_node = make_node(big, DEFAULT_COLOR)
			set_node_position(html_node, tree[big]["x"], tree[big]["y"])
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
			html_node = make_node(big, DEFAULT_COLOR)
			set_node_position(html_node, tree[big]["x"], tree[big]["y"])
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
			html_node = make_node(big, DEFAULT_COLOR)
			set_node_position(html_node, tree[big]["x"], tree[big]["y"])
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
	draw_lines(tree, person)


# Gives mouseover behavior to (person)'s node
def add_real_mouseover_event(tree, person):
	tree[person]["my_node"][1].addEventListener("mouseover", lambda e: real_mouseover_event(e, tree, person))

# Gives mouseover behavior to (ghost_dict)'s node
def add_ghost_mouseover_event(tree, real_person, ghost_dict):
	ghost_dict["my_node"][1].addEventListener("mouseover", lambda e: ghost_mouseover_event(e, tree, real_person, ghost_dict))

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
tree_dict = None
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
	iteration_count += 1
	svg = document.getElementById("svg-drawing")
	if(iteration_count == 1):
		resetAnimations()
		removeNodes()
		resetDict(tree_dict)
		if(tree_dict != None and input_name != None):
			draw_full_tree(tree_dict, input_name)
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






# TODO simple lines!
# TODO case with 3 or more bigs for ghost parents and top_big


# TODO Elliot case: not necessary i think but it will look a lot nicer on tree. it is an edge case tho so maybe we wont run into it too much

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


# This has the building blocks for svg content using the DOM

# TODO draw_tree_down lil 1 and lil 2 animation on lil 1 2 tree

# TODO case with lil 1 1 as root BAD

# Constants
NODE_WIDTH = 75
NODE_HEIGHT = 50
STROKE_WIDTH = 2

CHILD_LINE_COLOR = "black"
REAL_PARENT_LINE_COLOR = "blue"
GHOST_PARENT_LINE_COLOR = "green"

REAL_LINE_CONNECT_COLOR = "red"


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
			
