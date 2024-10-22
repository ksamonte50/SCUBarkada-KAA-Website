# Barkada of SCU's Official KAA Website
## Back-end architecture
- Our Cloud Run image runs using Flask and gunicorn.
- Using Docker, it creates an image that Cloud Run uses to respond to HTTP requests.

The architecture of the website is something like this:
```
-> Website calls Cloud Run server
  -> Cloud Run Server calls Google Sheets API
    -> Google Sheets API returns Data
  <- Cloud Run Server returns a json file with data for everyone in tree
<- Website visualizes the tree
```

The Cloud Run Server is necessary to for two reasons
- We are using pyscript for all the database work, and pyscript doesn't play nice with the sheets API
- There are secrets (api keys, credentials, etc.) that the API uses that we do not want on the files of our website

Using the data recieved, we place it into a python object and operate on it from there
This is so much faster and more efficient than our previous approach, which was to make an API call 
  everytime we wanted to get data.
### Getting Data from the Backend

We use the fetch api in pyscript to get all the data in the form of a json string. We can convert this to a 2D list in python to be operated on.

This can take up to 5 seconds since our server has cold starts to save on costs.

### Processing Data from the Backend
We get an input from the user, and from that build a dictionary of dictionaries to store data.
```
Class Tree:
  dict = {
    "name_of_person": {
      "row": Row number in 2D array that corresponds to their row in the Google sheets. Has data of bigs and littles.
      "x": x position of the person's svg. Default of 0.
      "y": y position of the person's svg. Default of 0.
      "visited": A check if the person's svg has been created. Default is False (not created).
      "parent_ghost_nodes": [  # An array of dicts that storee the svgs of person's parent ghost nodes.
        {
          "name": name of ghost
          "my_node": An array that stores the value of the svgs that make up the node. stored like: [background_rectangle, text_content]
          "x": x position of the ghost's svg.
          "y": y position of the ghost's svg.
          "lines": An array of the svgs of the lines that should be highlighted from hovering over person's node.
        }
        ...
      ]
      "child_ghost_nodes": [
        # same as parent_ghost_nodes
        ...
      ]
      "top_big": True if a node is the original draw_tree_down() caller from the function draw_tree_up() (if the node is on the "diagonal lines" moving up and outward from person).
      "my_node": An array that stores the value of the svgs that make up the node. stored like: [background_rectangle, text_content]
      "lines": An array of the svgs of the lines that should be highlighted from hovering over person's node.
      "bigs": An array that has all the names of person's bigs (Adjacency list for bigs)
      "littles": An array that has all the names of person's littles (Adjacency list for littles)
    }
    ...
  }
```

## Drawing the Tree
The part for drawing the tree uses an algorithm that is based on the Reingold-Tilford Algorithm, but it has been modified for our purposes.

### Basic Operation
```
function basic_operation():
  Give a node an X position of 0 and set an int x_inc to 0
  For each child:
    Give it an x position of 0 + x_inc
    Give it a y position of (parent's y - 2), then add 1 to x_inc.
  Center the original node over its children.
```
This is our "base algorithm" that we use and change to fit each edge case in our tree.

### Recursion
When using the basic_operation() recursively, the function returns the farthest right node it created. This is done to ensure that no nodes overlap when drawing their trees.
- The recursion is done in postorder for alignment purposes.

### Drawing Downwards
```
# Precondition: person has an x and y position, and is not visited yet.
x_increments = distance for 1 x increment (in pixels)
y_increments = distance for 1 y increment (in pixels)
function draw_tree_down(person):
  Visit node and create SVG content
  unvisited_littles = All unvisited littles of person
  visited_littles = All visited littles of person
  Initialize begin_x to person's x

  For each little in unvisted_littles:
    Give little an x position of begin_x
    Give little a y position of (parent's y + 2 y_increments)
    begin_x = recursive_basic_operation(child) + 1 x_increments
    If a little in unvisited_littles was visited, remove them from unvisited_littles and add them to visited_littles.
    Make ghost bigs if little has any and offset little to center it under the ghost parents

  For each little in visited_littles:
    Make HTML node for ghost little
    begin_x += 1 x_increments
    Give it x position of the new begin_x
    Give little a y position of (parent's y + 2 y_increments)

  Center person over its children.
  Draw person node to SVG
  return begin_x - 1 x_increment
```
** Explanation: **
Since nodes in our tree can have more than one parent, there must be some way to place the other parents on the tree. 
We decided to place the node right above the child it relates to, and we call these nodes "**Parent Ghost Nodes**".

<img width = "231" src="https://github.com/user-attachments/assets/23487b64-5afb-41b1-8096-dc002041024c" alt="Screenshot of a Parent Ghost Node in stated context">

*In this example, "big 1" is the ghost big of "lil 1 2"*

The "Real parent" of the node is actually 2 y-increments above the child, and the ghost nodes are placed 1 y-increment above. This is done because it is easier to deal with overlap issues this way.

Some nodes may have more than 1 of these ghost nodes, so we have to use the basic operation upward this time.

### Drawing Upwards
```
# queue has data [person to be drawn, little who added person to queue].
# direction is either -1 or +1 depending on branching left or right.
function draw_tree_up(tree, queue, direction, outward_offset):
  front = front of queue
  person = front[0]
  current_little = front[1]
  starting_x = person's x

  if person has been visited
    make a parent ghost node for (current_little) instead of another branch.

  call draw_tree_down(person) and store return value in far_x

  # out = the far right/left x plus one x_increment in the direction we are branching; x_increment is done at the end.
  out = far_x
  if we are branching left
    # far_x is greater than starting_x; starting_x - far_x = negative number; offset will be towards the left.
    offset all nodes drawn by starting_x - far_x to not overlap.
    out = starting_x + (starting_x - far_x)

  add parent nodes of (person) to queue and preserve order seen in (person)'s adjacency list.

  if we created more than 1 parent ghost node, align (person) inbetween the parent ghosts.

  if queue is not empty
    draw_tree_up(tree, queue, direction, outward_offset = out + (direction * x_increments))

return  
```
** Explanation: **
A helper function calls draw_tree_up in two separate directions, splitting the bigs into two separate queues and calling draw_tree_up twice, once branching left and another branching right.

<img width="1071" alt="Example of how Bigs of bigs are connected" src="https://github.com/user-attachments/assets/4937e710-6c50-4c25-b121-85f24a9c8de6">

*In this example, Saunder and Justin are the parents of MJ, while Jeremy and Renceh are the parents of Adrian*

The parents of parents are connected diagonnally in this way to avoid overlap. If we were drawing straight up, there would be a lot of realignment to make the tree compact. This approach avoids that realignment at the cost of having a wider tree.
