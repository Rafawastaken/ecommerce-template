from flask import render_template, session, url_for, redirect

# Local imports
from shop import app, db

@app.route("/")
def home():
    return "home page of website"

@app.route('/register')
def register():
    return render_template('admin/register.html', title = "Register Page")