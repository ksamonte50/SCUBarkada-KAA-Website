from os import environ
from sys import argv
import json

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

if __name__ == "__main__":
	if(len(argv) == 1):
		print('Usage: python3 createToken "/path/to/file.json"\nReturns a .json file\nMake sure the environment variables are set and you have access to the account\n')
		exit()
	SCOPES = environ.get('SHEET_SCOPES')
	creds = None
	if creds and creds.expired and creds.refresh_token:
		creds.refresh(Request()) # opens the google sign in page
	else:
		try:
			config = json.loads(environ['SHEET_CRED'])
		except:
			print("Enviornment Variables not loaded!")
			exit()
		flow = InstalledAppFlow.from_client_config(
			config, SCOPES
		)
		creds = flow.run_local_server(port=0)
	try:
		with open(str(argv[1]), "w") as token:
			token.write(creds.to_json())
		print("Success! Set the secret token on the project to the created token.")
	except:
		print("Error: File Not Created! \nCheck the filepath to see if it is valid or already taken")