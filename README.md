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
- The recursion is done postorder
- A sib of a node could be visited during another child's basic_operation(). We must check if nodes become visited after each node is looked at.
```
function recursive_basic_operation():
  Give a node an X position of 0 and set an int x_inc to 0
  Declare begin_x
  For each child:
    Give it an x position of 0 + x_inc
    Give it a y position of (parent's y - 2), then add 1 to x_inc.
    begin_x = recursive_basic_operation() on child + 1 x_increment
  Center the original node over its children.

  return begin_x - 1 x_increment
```

### Drawing Downwards
Since nodes in our tree can have more than one parent, there must be some way to place the other parents on the tree. 
We decided to place the node right above the child it relates to, and we call these nodes "**Parent Ghost Nodes**".

<img width = "231" src="https://github.com/user-attachments/assets/23487b64-5afb-41b1-8096-dc002041024c" alt="Screenshot of a Parent Ghost Node in stated context">

*In this example, "big 1" is the ghost big of "lil 1 2"*

The "Real parent" of the node is actually 2 y-increments above the child, and the ghost nodes are placed 1 y-increment above. This is done because it is easier to deal with overlap issues this way.

Some nodes may have more than 1 of these ghost nodes, so we have to use the basic operation upward this time.
