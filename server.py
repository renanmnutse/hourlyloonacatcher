from os import environ
from flask import Flask

@app.route("/")
def index():
  return "<meta http-equiv="refresh" content="time; URL=https://hourlyloonacatcher.carrd.co/" />"

if __name__ == "__main__":
  app = Flask(__name__)
  app.run(environ.get('PORT'))
