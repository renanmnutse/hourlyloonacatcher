from os import environ
from flask import Flask

@app.route("/")
def index():
  return "index.html"

if __name__ == "__main__":
  app = Flask(__name__)
  app.run(environ.get('PORT'))
