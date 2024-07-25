import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]

def main():
  # Give Google API the credentials
  global creds
  creds = None
  # token.json file is created if not already in directiroy
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  else: 
    createNewToken()
  # service = build("sheets", "v4", credentials=creds)
  # Call the Sheets API
  global sheet
  sheet = build("sheets", "v4", credentials=creds).spreadsheets()

# returns the sheet variable for interacting with the google sheet
def getSheet():
  global sheet
  return sheet

def createNewToken():
# If there are no (valid) credentials available, let the user log in.
  global creds
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
  try:
    global sheet
    result = (
        sheet.values()
        .get(spreadsheetId=id,range=sheetsRange)
        .execute()
    )
    values = result.get("values", [])
    if not values:
      # print("sheetsbase.getData: No data found.")
      return 
    return values # returns a 2D array!!! if you request a single cell, do values[0][0] for the string!
  
  except HttpError as err:
      print(f"sheetsbase.getData: An error occured: {err}")
      return

if __name__ == "__main__":
   main()