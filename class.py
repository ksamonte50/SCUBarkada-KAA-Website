import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
spreadsheet_ID = "1VidXQeKAelgcGtEf7bkFqQX7VB82ATwCX8ok4mcIqpM"

def createNewToken():
# If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request()) # opens the google sign in page
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  return

# gets data of one cell
# Precondition: 
# Postcondition: returns an array of strings.
def getData(id, sheetsRange):
  # Give Google API the credentials
  creds = None
  # token.json file is created if not already in directiroy
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  else: createNewToken()

  # actual code
  try:
    service = build("sheets", "v4", credentials=creds)
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=id,range=sheetsRange)
        .execute()
    )
    values = result.get("values", [])

    if not values:
      print("No data found.")
      return
  
    return values # returns a 2D array!!! if you request a single cell, do values[0] for the array!
  
  except HttpError as err:
      print(f"An error occured: {err}")
      return

# This function splits names into separate strings.
def splitComma(input): 
  arr = input.split(",")
  if len(arr) == 1 or len(arr) == 0:
    return arr
  newArr = []
  for elt in arr:
    newArr.append(elt.strip())
  return newArr

# return the row number of the name
def searchName(id, name):
    # Give Google API the credentials
    creds = None
    # token.json file is created if not already in directiroy
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else: 
      createNewToken()
    # try:
        #cell = sheet.find(name)
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=id,range="A:A")
        .execute()
    )
    values = result.get("values", [])
    # [['hi', 'elliot']]
    values.pop(0) # or we can not include "Person" in the request
    # ['hi', 'elliot'] (all the names in alphabetical order)
    counter = 0
    out = binarySearch(values, 0, len(values) - 1, name, counter)
    return out
    # except: 
    #   print("Error! uh oh")      
              
# binary search!
def binarySearch(values, lo, hi, target, counter):
    counter = counter + 1
    # if counter > 5: 
    #   exit()
    mid = (hi + lo) // 2
    print("1")
    print("mid = " + str(mid))
    print("lo = " + str(lo))
    print("hi = " + str(hi))
    print(values[mid][0])
    print("2")
    print(values[mid][0] == target)
    match values[mid][0] == target: 
        case False:
            if target > values[mid][0]: # search right
                return binarySearch(values, mid + 1, hi, target, counter)
            
            if target < values[mid][0]: # search left
                print('3')
                return binarySearch(values, lo, mid - 1, target, counter)
        case True:
            print(mid)
            return mid
        case _:
            print('Not found womp womp')
            return


class Person:
    def __init__(self, name):
        self.name = name
        self.row = searchName(spreadsheet_ID, name) + 2
        print(self.row)
        
        temp = getData(spreadsheet_ID, "C" + str(self.row))
        if temp == None:
          self.bigs = []
        else:
          self.bigs = splitComma(temp[0][0]) # [big1, big2] 
        
        temp = getData(spreadsheet_ID, "B" + str(self.row))
        if temp == None:
          self.littles = []
        else:
          self.littles = splitComma(temp[0][0]) # [big1, big2]
        # self.famname = ""

    def getBigs():
        return 

elliot = Person("Eunice Sabado")

print(elliot.name) # "Elliot Bernardo"
print(elliot.bigs) # [Gabby Arceo, Matthew Beltran]
print(elliot.littles) # []
