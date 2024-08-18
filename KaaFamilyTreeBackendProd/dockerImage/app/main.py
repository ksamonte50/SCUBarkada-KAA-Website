# This file creates the server necessary for Google Cloud Run
from flask import Flask, jsonify
from flask_cors import CORS
from os import environ

import sheetsbase

app = Flask(__name__)

# if there are no HOST_URL environment variable on the google server, 
# allow all servers to connect.
authorized_origins = environ.get('HOST_URL')
if(authorized_origins == None): 
	authorized_origins = "*"
CORS(app, origins=authorized_origins, methods=["GET", "POST"])

@app.route("/")
def sendDataToPage():
	# place the value in a "data" attribtute to allow for jsonification
	out = {
		"data": sheetsbase.getData("A:C")
	}
	return jsonify(out)