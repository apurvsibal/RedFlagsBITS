from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

users = []
purchases = []




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










