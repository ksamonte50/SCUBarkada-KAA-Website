# This file facilitates the API request
from os import environ
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [environ.get('SHEET_SCOPES')]
# creds variable used for request; it is set later in the code
creds = None

# If the SHEET_TOKEN doesn't work, reset the token through Google Cloud Shell
if (environ.get("SHEET_TOKEN") != None):
  info = json.loads(environ['SHEET_TOKEN'])
  try:
    creds = Credentials.from_authorized_user_info(info, SCOPES)
  except:
    print("Token is expired or invalid. Please contact an administrator.")
    exit()
else:
  print("Environment Variables are not loaded!")
  exit()

# Gets data of the selected range
def getData(sheetsRange):
  try:
    sheet = build("sheets", "v4", credentials=creds).spreadsheets()
    result = (
      sheet.values()
      .get(spreadsheetId=environ.get('SHEET_ID'), range=sheetsRange)
      .execute()
    )
    values = result.get("values", [])
    if not values:
      return None
    return values # returns a 2D list!!! if you request a single cell, access it with values[0][0]!
  except HttpError as err:
    print(f"sheetsbase.getData: An error occured: {err}")
    return