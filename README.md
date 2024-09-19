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
  Give a node an X position of 0 and set an int x_inc to 0
  For each child:
    Give it an x position of 0 + x_inc
    Give it a y position of (parent's y - 2), then add 1 to x_inc.
  Center the original node over its children.
```
This is our "base algorithm" that we use and change to fit each edge case in our tree.

### Drawing Downwards
Since nodes in our tree can have more than one parent, there must be some way to place the other parents on the tree. 
We decided to place the node right above the child it relates to, and we call these nodes "**Parent Ghost Nodes**".

<img width="231" alt="Screenshot of a Parent Ghost Node in stated context" src="https://github.com/user-attachments/assets/751dae54-7e42-4907-8c69-5b71765a7ae5">
