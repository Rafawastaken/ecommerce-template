from flask import render_template, session, url_for, redirect

# Local imports
from shop import app, db

@app.route("/")
def home():
    return "teste"