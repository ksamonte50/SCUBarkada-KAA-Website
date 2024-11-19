# This file gets the data from the backend
from pyscript import fetch, document, window
import asyncio
import json
from draw import prepare_svg

# NOTE: we can use web-workers to take a load off the main page but pyscript doesn't
#		play nicely with web-workers. 
#		if we use web-workers later down the line, there will be a problem using the 
#		DOM. This is because there are necessary headers and config settings that
#		make the DOM not work with web workers.

# TODO GET_URL could be an environment varible
GET_URL = "https://python-sheets-data-gixw5eexra-uw.a.run.app"
# GET_URL = "https://jsonplaceholder.typicode.com/users"

data = None
# This variable used to store data from the API
# NOTE: in the data returned, anything in the last column will be omitted if there is no value 
# 		(for us, if the person has no bigs, their row will only have 2 indexes instead of 3).
#		to address this, code has been put in treeclass.splitComma() that addresses this.

# Getter functions of data (not used atm)
def getAllData():
	return data
def getData(row, col):
	if(0 <= row and row < len(data) and 0 <= col and col < len(data[0])):
		return data[row][col]
	return None

# Function that makes the request to the API
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

# Edit the DOM after data is retrieved
async def main():
	print("hi")
	await getAPIData()
	document.getElementById("load-screen").style.display = "none"
	document.getElementById("testButton").style.display = "inline"
	input_field = document.getElementById("tree_name")
	print("before")
	set_autocomplete(input_field)
	prepare_svg()
	return

# necessary to run async code on browser.
def getData(event):
	asyncio.create_task(main())

# Run the async code as soon as all our modules are loaded
window.addEventListener("py:all-done", getData)


item_box = None
values = []
# Takes two arguments, input element and array of strings
def set_autocomplete(input):
	input_field = document.getElementById("tree_name")
	global values
	for row in data:
		values.append(row[0])
	input.addEventListener("input", lambda e: inputEvent(input_field))

def inputEvent(input):
	clear_autocomplete()
	global item_box
	value = input.value
	value_length = len(value)
	container = document.getElementById("autocomplete-container")
	item_box = document.createElement("DIV")
	item_box.setAttribute("id", "autocomplete-box")
	document.body.addEventListener("click", clear_autocomplete)
	container.appendChild(item_box)
	global values
	for person in values:
		if(person.strip().lower()[0:value_length] == value.lower()):
			new_option = document.createElement("DIV")
			new_option.setAttribute("class", "autocomplete-item")
			new_option.innerHTML = person
			new_option.addEventListener("click", lambda e: click_option(e))
			item_box.appendChild(new_option)

def click_option(event):
	if(event != None):
		name = event.target.innerHTML
		print(name)
		document.getElementById("tree_name").value = name
		clear_autocomplete()

def clear_autocomplete(e=None):
	document.body.removeEventListener("click", clear_autocomplete)
	item_box = document.getElementById("autocomplete-box")
	if(item_box != None):
		while(item_box.firstChild):
			item_box.removeChild(item_box.lastChild)
		item_box.parentNode.removeChild(item_box)
		