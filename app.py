# This file gets the data from the backend
from pyscript import fetch, document, window
import asyncio
import json

# NOTE: we can use web-workers to take a load off the main page but pyscript doesn't
#		play nicely with web-workers. 
#		if we use web-workers later down the line, there will be a problem using the 
#		DOM. This is because there are necessary headers and config settings that
#		make the DOM not work with web workers.

# TODO GET_URL could be an environment varible (if we can access those)
GET_URL = "https://python-sheets-data-gixw5eexra-uw.a.run.app"
# GET_URL = "https://jsonplaceholder.typicode.com/users"

data = None
# This variable used to store data from the API
# NOTE: in the data returned, anything in the last column will be omitted if there is no value 
# 		(for us, if the person has no bigs, their row will only have 2 indexes instead of 3).
#		to address this, code has been put in treeclass.splitComma() that addresses this.

# getter functions of data (not used atm)
def getAllData():
	return data
def getData(row, col):
	if(0 <= row and row < len(data) and 0 <= col and col < len(data[0])):
		return data[row][col]
	return None

# function that makes the request to the API
# 	Status code is 200 if the request was sucessful
async def getAPIData():
	rawResult = None
	try:
		rawResult = await fetch(
			url=GET_URL, 
			method="GET",
			headers={"Content-Type": "application/json; charset=UTF-8"}
		)
		result = await rawResult.text()
		global data
		data = json.loads(result)["data"] # the extra ["data"] is here because of the way the json is formatted
		data.pop(0) # removes the column names from the data
		return
	except:
		print(f"app.py: Something went wrong (ERRNO {rawResult.status}).")
		return

# edit the DOM to account for sucessful data retrieval
async def main():
	await getAPIData()
	document.getElementById("testButton").style = "visibility: visible"
	return

# necessary to run async code on browser.
def getData(event):
	asyncio.create_task(main())

window.addEventListener("py:all-done", getData)