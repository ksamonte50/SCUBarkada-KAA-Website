import os.path
import sheetsbase

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
spreadsheet_ID = "1VidXQeKAelgcGtEf7bkFqQX7VB82ATwCX8ok4mcIqpM"

def main():
  sheetsbase.main() # creates connection to google sheets.
  result = (
      sheetsbase.getSheet().values()
      .get(spreadsheetId=spreadsheet_ID,range="A:A")
      .execute()
  )
  global names # variable for storing all names in an array
  names = result.get("values", [])
  names.pop(0) # or we can just not include "Person" in the range

# function that splits the names gathered from database into separate strings.
def splitComma(input): 
  if input == None or input == []:
     return []
  arr = input[0][0].split(",")
  if len(arr) == 1 or len(arr) == 0:
    return arr
  newArr = []
  for elt in arr:
    newArr.append(elt.strip())
  return newArr

# function that returns the row number of the name
def searchName(name):
    global names
    name.strip()
    out = binarySearch(names, 0, len(names) - 1, name)
    return out
      
# binary search!
def binarySearch(values, lo, hi, target):
    if hi >= lo:
      mid = (hi + lo) // 2
      # print("mid: " + str(mid) + " and its " + values[mid][0])
      # print("target: " + target)
      temp = values[mid][0].strip()
      if(temp == target):
        return mid
      match temp == target: 
          case False:
              if target > temp: # search right
                  # print("goin right: " + str(mid + 1) + " to " + str(hi) + " and its from " + values[mid+1][0] + " to " + values[hi][0])
                  return binarySearch(values, mid + 1, hi, target)
              if target < temp: # search left
                  # print("going left: " + str(lo) + " to " + str(mid - 1) + " and its from " + values[lo][0] + " to " + values[mid - 1][0])
                  return binarySearch(values, lo, mid - 1, target)
          case True:
              return mid
          case _:
              print('binarySearch: Not found womp womp')
              return
    else: 
       return -3 # nada

class Tree:
  def __init__(self, input):
    self.root = input # name of person we want to build tree for
    self.check = [] # array used for checking who we have processed already
    self.dict = {} # used to store all of the data
  
  # recursive function to build the dictionary with all of our nodes
  def makeTree(self, input):
    self.check.append(input)
    print("findFam: " + input)
    if input == None or input == []: # base case to stop recursion
      return
    # process data for (input)
    self.dict[input] = {}
    self.dict[input]["row"] = searchName(input) + 2
    self.dict[input]["bigs"] = splitComma(sheetsbase.getData(spreadsheet_ID, "C" + str(self.dict[input]["row"])))
    self.dict[input]["littles"] = splitComma(sheetsbase.getData(spreadsheet_ID, "B" + str(self.dict[input]["row"])))
    # if (input)'s bigs or littles have not been processed yet, process them.
    for bigName in self.dict[input]["bigs"]:
      if(bigName not in self.dict):
        self.makeTree(bigName)
    for lilName in self.dict[input]["littles"]:
      if(lilName not in self.dict):
        self.makeTree(lilName)

  # function to print all elements in the tree
  def printTree(self):
      for person in self.dict:
          print(person)
          print("  row#: " + str(self.dict[person]["row"]))
          print("  bigs: " + str(self.dict[person]["bigs"]))
          print("  lils: " + str(self.dict[person]["littles"]))

# calls main function
if __name__ == "__main__":
   main()

# test code :)
tree = Tree("Joshua Sixto Beltran")
tree.makeTree(tree.root)

tree.printTree()
