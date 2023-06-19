import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")




@app.route("/")
@login_required
def index():

    return render_template("index.html")


@app.route("/diagnosis")
def diagnosis():
    """Show diagnostic information"""
    diagnosis_info = {

    }

    return render_template("diagnosis.html", diagnosis_info=diagnosis_info)

@app.route("/Acute_Backpain")
def Acute_Backpain():
    information = ""

    return render_template("Acute.html", information=information)

@app.route("/Subacute_Backpain")
def Subacute_Backpain():
    information = ""
    return render_template("Subacute.html", information=information)

@app.route("/Chronic_Backpain")
def Chronic_Backpain():
    information = ""
    return render_template("Chronic.html", information=information)

@app.route("/Upper_Backpain")
def Upper_Backpain():
    information = ""
    return render_template("Upper.html", information=information)

@app.route("/Middle_Backpain")
def Middle_Backpain():
    information = ""
    return render_template("Middle.html", information=information)


@app.route("/Lower_Backpain")
def Lower_Backpain():
    information = ""
    return render_template("Lower.html", information=information)










