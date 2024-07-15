import os.path
import sheetsbase

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
spreadsheet_ID = "1VidXQeKAelgcGtEf7bkFqQX7VB82ATwCX8ok4mcIqpM"

# This function splits names into separate strings.
def splitComma(input): 
  arr = input.split(",")
  if len(arr) == 1 or len(arr) == 0:
    return arr
  newArr = []
  for elt in arr:
    newArr.append(elt.strip())
  return newArr

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
  names.pop(0) # or we can not include "Person" in the request


# return the row number of the name
def searchName(name):
    global names
    out = binarySearch(names, 0, len(names) - 1, name)
    return out      
              
# binary search!
def binarySearch(values, lo, hi, target):
    # if counter > 5: 
    #   exit()
    mid = (hi + lo) // 2
    
    match values[mid][0] == target: 
        case False:
            if target > values[mid][0]: # search right
                return binarySearch(values, mid + 1, hi, target)
            
            if target < values[mid][0]: # search left
                return binarySearch(values, lo, mid - 1, target)
        case True:
            return mid
        case _:
            print('binarySearch: Not found womp womp')
            return


class Person:
    def __init__(self, name):
        self.name = name
        self.flag = False
        self.row = searchName(name) + 2 # add 2 because we removed "Person" and array index starts counting from 0.
        
        temp = sheetsbase.getData(spreadsheet_ID, "C" + str(self.row))
        if temp == None:
          self.bigs = []
        else:
          self.bigs = splitComma(temp[0][0]) # [big1, big2] 
          #self.bigs = [Person(big1), Person(big2)]
        
        temp = sheetsbase.getData(spreadsheet_ID, "B" + str(self.row))
        if temp == None:
          self.littles = []
        else:
          self.littles = splitComma(temp[0][0]) # [big1, big2]
        # self.famname = ""

    def getBigs(self):
        return self.bigs

if __name__ == "__main__":
   main()

# main code :)
elliot = Person("Elliot Bernardo")
print(elliot.name) # "Elliot Bernardo"
print(elliot.bigs) # [Gabby Arceo, Matthew Beltran]
print(elliot.littles) # []

gamer = Person("Edwin Simeon")
print(gamer.name) # "Elliot Bernardo"
print(gamer.bigs) # [Gabby Arceo, Matthew Beltran]
print(gamer.littles) # []