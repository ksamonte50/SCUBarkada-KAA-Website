import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# IF MODIFYING THESE SCOPES, delete the file token.json.
SCOPES = 'INSERT_HERE'
spreadsheet_ID = 'INSERT_HERE'


def main():
  # actual code
  text = getData(spreadsheet_ID, "B10:B10")
  littles = splitLittles(text[0][0])
  print(littles)

# gets data of one cell
# Precondition: 
# Postcondition: returns an array of strings.
def getData(id, sheetsRange):
  # Give Google API the credentials
  creds = None
  # token.json file is created if not already in directiroy
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  # If there are no (valid) credentials available, let the user log in.
  # if not creds or not creds.valid:
  #   if creds and creds.expired and creds.refresh_token:
  #     creds.refresh(Request()) #opens the google sign in page
  #   else:
  #     flow = InstalledAppFlow.from_client_secrets_file(
  #         "credentials.json", SCOPES
  #     )
  #     creds = flow.run_local_server(port=0)
  #   # Save the credentials for the next run
  #   with open("token.json", "w") as token:
  #     token.write(creds.to_json())

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
    
    #return splitLittles(values[0][0]) # this is WIERD! will be fixed later
    return values
  
  except HttpError as err:
      print(f"An error occured: {err}")
      return

# This function splits the littles into separate strings.
def splitLittles(input):
  arr = input.split(",")
  newArr = []
  for elt in arr:
    newArr.append(elt.strip())
  return newArr

if __name__ == "__main__":
  main()
