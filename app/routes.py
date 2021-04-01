from flask import render_template
from app import app
from app import database as db_helper


@app.route("/")
def homepage():
  return render_template("index.html", name="Alice")
