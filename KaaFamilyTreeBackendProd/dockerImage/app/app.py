# This is the file that is run in the Docker image
from main import app
if __name__ == "__main__":
	app.run()