from flask import render_template, redirect

from app import app
from app.forms import LoginForm


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')