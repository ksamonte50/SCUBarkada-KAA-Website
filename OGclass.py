import os.path
import sheetsbase

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
spreadsheet_ID = "1VidXQeKAelgcGtEf7bkFqQX7VB82ATwCX8ok4mcIqpM"

# no need to redo code :)
def main():
  sheetsbase.main()
  result = (
      sheetsbase.getSheet().values()
      .get(spreadsheetId=spreadsheet_ID,range="A:A")
      .execute()
  )
  global names
  names = result.get("values", [])
  names.pop(0) # or we can just not include "Person" in the range

# This function splits names into separate strings.
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

# return the row number of the name
def searchName(name):
    global names
    global counter
    counter = 0
    name.strip()
    out = binarySearch(names, 0, len(names) - 1, name)
    return out      
# binary search!
def binarySearch(values, lo, hi, target):
    if hi >= lo:
      global counter
      counter = counter + 1
      if counter > 20:
        exit()
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
    def __init__(self, inputName):
      self.check = []
      self.root = Person(inputName,[], [])

class Person:
    def __init__(self, name, bigs, littles):
        self.name = name
        # self.flag = False
        self.row = searchName(name) + 2 # add 2 to row number because we removed "Person" and array index starts counting from 0.
        self.bigs = []
        self.littles = []
        # temp = sheetsbase.getData(spreadsheet_ID, "C" + str(self.row))
        # if temp == None:
        #   self.bigs = []
        # else:
        #   self.bigs = splitComma(temp[0][0]) # [big1, big2] 
        #   # self.bigs = [Person(big1), Person(big2)]
        
        # temp = sheetsbase.getData(spreadsheet_ID, "B" + str(self.row))
        # if temp == None:
        #   self.littles = []
        # else:
        #   self.littles = splitComma(temp[0][0]) # [big1, big2]
        #   # self.famname = ""

    def findFam(self, arr):
      arr.append(self.name) 		#  use this array to check who has been processed 
      
      print("findFam: " + self.name)
      temp = sheetsbase.getData(spreadsheet_ID, "C" + str(self.row))
      print("bigs: " + str(temp))
      temp = splitComma(temp)
      for bigName in temp:
        if(bigName not in arr):		# check if name has been processed
          # if not, create an object for them while passing in your name
          self.bigs.append( Person(bigName, [], [self]) )
          self.bigs[-1].findFam(arr) # recursive call. Operates on the created person

      temp2 = sheetsbase.getData(spreadsheet_ID, "B" + str(self.row))
      print("littles: " + str(temp2))
      temp2 = splitComma(temp2)
      for lilName in temp2:
        print("lilName: " + lilName)
        print(arr)
        if(lilName not in arr):		# check if name has been processedo
          newPerson = Person(lilName, [self], [])
          self.littles.append(newPerson)
          newPerson.findFam(arr) # recursive call. Operates on the created person	
      return

    def getBigs(self):
        return self.bigs

if __name__ == "__main__":
   main()

# test code :)
tree = Tree("Joshua Sixto Beltran")
tree.root.findFam(tree.check)

print(tree.root.bigs[0].name)