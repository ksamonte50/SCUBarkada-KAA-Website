# This code makes the edge list used for drawing the tree.
import app
from draw import click_event as set_tree
from pyscript import when, document

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
    out = binarySearch(app.data, 0, len(app.data) - 1, input.lower()) 
    return out
      
# binary search!
# .lower() is used for string comparison 
#   (should use casefold() instead, but micropython doesn't support that cmd)
def binarySearch(values, lo, hi, target):
    if lo <= hi:
        mid = (hi + lo) // 2
        temp = app.data[mid][0].strip().lower()
        if(temp == target):
            return mid
        if target > temp: # search right
            return binarySearch(values, mid + 1, hi, target)
        if target < temp: # search left
            return binarySearch(values, lo, mid - 1, target)
    return -1 # nada

# using class for when we need more than one tree
class Tree:
  def __init__(self, input):
    self.in_tree = False
    for row in app.data:
       if(row[0].lower() == input.lower()):
          self.in_tree = True
          self.root = row[0] # name of person we want to build tree for
          break
    if(self.in_tree):
      self.dict = {} # used to store the edge list
    return
    
  
  # recursive function to build the dictionary with all necessary nodes
  def makeTree(self, input):
    print(f"treeclass: finding fam of {input}")

    # process data for (input)
    row = searchNameForIndex(input)
    if(row == -1):
      print(f"treeclass: did not find {input}")
      return
    print(f"  row: {row}")
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
    # self.dict[input]["parentGhostNodes"] = []
    # self.dict[input]["childGhostNodes"] = []
    # set bigs array
    if(len(app.data[row]) < 3):
      self.dict[input]["bigs"] = []
    else:
      self.dict[input]["bigs"] = splitComma(app.data[row][2])
    # set littles array
    if(len(app.data[row]) < 2):
      self.dict[input]["littles"] = []
    else:
      self.dict[input]["littles"] = splitComma(app.data[row][1])

    # if (input)'s bigs or littles have not been processed yet, process them.
    for bigName in self.dict[input]["bigs"]:
      if(bigName not in self.dict):
        self.makeTree(bigName)
    for lilName in self.dict[input]["littles"]:
      if(lilName not in self.dict):
        self.makeTree(lilName)

  # function to print data of all nodes in the tree
  def printTree(self):
      for person in self.dict:
          print(person)
          print("  row#: " + str(self.dict[person]["row"]))
          print("  bigs: " + str(self.dict[person]["bigs"]))
          print("  lils: " + str(self.dict[person]["littles"]))
      return

# pyscript syntax for setting a click listener on button with id = "testButton"
@when("click", "#testButton")
def testTree():
  print("Button Pushed.")
  global input_name
  input_name = document.getElementById("tree_name").value
  if(app.data == None):
    print(f"Data not recieved yet. Aborting...")
    return
  tree = Tree(input_name) # tests code. output found in console
  if(not tree.in_tree):
     print("Person is not in tree.")
     return
  tree.makeTree(tree.root)
  set_tree(None, tree.dict, person=tree.root)
  return