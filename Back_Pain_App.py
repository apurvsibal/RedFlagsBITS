"""
Purpose:
    API for the application.
"""

import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

from flask import Flask, render_template, request, url_for, flash, redirect, session
import re
# from flask import send_file, send_from_directory, abort
# import io
import os
from datetime import date, timedelta, datetime

import model

from flask_babel import Babel, gettext
import constants

from werkzeug.security import check_password_hash, generate_password_hash
import secrets


secret_key = secrets.token_hex(16)
app = Flask(__name__)
app.secret_key = secret_key

path = str(os.path.dirname(os.path.abspath(__file__)))
path = path.replace('\\', '/')
app.config['files'] = path + '/temp/'

db = sqlite3.connect('backpain.db', check_same_thread=False) # Connect to database
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS symptoms(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datetime_column TEXT,
    symptom1 TEXT,
    symptom2 TEXT,
    symptom3 TEXT,
    symptom4 TEXT);''')
# also too include: username TEXT,
db.commit() # Create "symptoms" table if not already created
cursor.execute('''CREATE TABLE IF NOT EXISTS oswentry_individual(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datetime_column TEXT,
    score1 INT,
    score2 INT,
    score3 INT,
    score4 INT,
    score5 INT,
    score6 INT,
    score7 INT,
    score8 INT,
    score9 INT,
    score10 INT);''')
# also too include: username TEXT,
db.commit() # Create "oswentry_individual" table if not already created
cursor.execute('''CREATE TABLE IF NOT EXISTS oswentry_total(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datetime_column TEXT,
    score INT);''')
# also too include: username TEXT,
db.commit() # Create "oswentry_total" table if not already created
db.close()

babel = Babel(app)
app.config['LANGUAGES'] = {'en': 'English', 'es': 'Spanish', 'fr': 'French', 'hi':'Hindi','zh':'Chinese'}

lang = 'en'
def get_locale():
    return constants.lang
babel.init_app(app, locale_selector=get_locale)

@app.route('/', methods=('GET', 'POST'))  # Route and accepted Methods
@app.route('/index', methods=('GET', 'POST'))
def index():
    """

    """
    if request.method == 'POST':
        constants.lang = request.json.get('language')
        print(constants.lang)
        return f"You selected: {constants.lang}"
    else:
        header_1 = gettext('Red Flags')
        header_2 = gettext('For Back Pain')
        explanation = gettext('Some cases of back pain can be serious, and require immediate medical attention. We are going to ask a few question to understand the nature of your pain.')
        return render_template('index.html', header_1=header_1, header_2=header_2, explanation=explanation)


@app.route('/red_flags', methods=('GET', 'POST'))
@app.route('/red_flags/<int:question_number>', methods=('GET', 'POST'))
def red_flags_questionnaire(question_number: int = 0):
    num_question = 3
    header_1 = gettext('Is your back pain associated with any of the following?')
    if question_number and request.args.get('answer') == gettext('Yes'):
        header_1 = gettext('You need immediate care')
        explanation = gettext("You answered 'Yes' to a question indicating you could be in need of emergency care. Use the map below to see some providers")
        map_link = 'https://goo.gl/maps/zKXs4iFKqaqDwfJy6'
        return render_template('immediate_care.html', header_1=header_1, explanation=explanation, map_link=map_link)
    elif not question_number:
        question_number = 1
    elif question_number > num_question:
        return redirect(url_for('mobile_msk_questionaire'))
    question, answers, more_information = model.get_red_flag_question(question_number)
    return render_template('Red_Flags.html', header_1=header_1, question=question, answers=answers,
                           more_information=more_information, next_question_number=question_number + 1)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        age = request.form.get("age")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Error conditions
        if not (name and email and age and username and password and confirm_password):
            flash("Please fill in all the required fields.")
            return render_template("register.html", name=name, email=email, age=age, username=username)

        if len(password) < 8:
            flash("Password must be at least 8 characters long.")
            return render_template("register.html", name=name, email=email, age=age, username=username)

        if password != confirm_password:
            flash("Passwords do not match")
            return render_template('register.html', name=name, email=email, age=age, username=username)

        if not re.search(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]+$', password):
            flash("Password must contain at least one letter, one number, and one special character")
            return render_template('register.html', name=name, email=email, age=age, username=username)

        if '@' not in email:
            flash("Invalid email address")
            return render_template('register.html', name=name, age=age, username=username)

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone() is not None:
            flash("Username already exists")
            return render_template('register.html', name=name, email=email, age=age)

        password_hash = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password, email, age, name) VALUES (?, ?, ?, ?, ?)",
                       (username, password_hash, email, age, name))
        conn.commit()
        conn.close()
        return redirect("https://sites.google.com/view/mobilemskdemo/home")

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        if username and password:
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            rows = cursor.fetchall()
            if rows:
                stored_username = rows[0][1]
                stored_password = rows[0][2]
                login_attempts = rows[0][6]
                lockout_end_time_str = rows[0][7]

                current_time = datetime.now()
                # Code for locking a user out after 3 failed password attempts
                if lockout_end_time_str:
                    lockout_end_time = datetime.fromisoformat(lockout_end_time_str)
                    if current_time < lockout_end_time:
                        time_left = (lockout_end_time - current_time).seconds
                        flash(f"Account locked. Please try again after {time_left} seconds")
                        conn.commit()
                        conn.close()
                        return redirect(url_for('login'))

                if check_password_hash(stored_password, password) and stored_username == username:
                    session['username'] = username
                    # Reset login attempts upon successful login
                    cursor.execute("UPDATE users SET login_attempts = 0, lockout_end_time = NULL WHERE username = ?", (username,))
                    conn.commit()
                    conn.close()
                    return redirect("https://sites.google.com/view/mobilemskdemo/home")
                else:
                    login_attempts += 1
                    if login_attempts >= 3:
                        # Disables login for a minute, can be changed based on requirements
                        lockout_duration = timedelta(minutes=1)
                        lockout_end_time = current_time + lockout_duration
                        cursor.execute("UPDATE users SET login_attempts = 0, lockout_end_time = ? WHERE username = ?", (lockout_end_time.isoformat(), username))
                        flash("Too many failed login attempts. Your account is locked for 1 minute")
                    else:
                        cursor.execute("UPDATE users SET login_attempts = ? WHERE username = ?", (login_attempts, username))
                        flash("Incorrect password")
            else:
                flash("Username doesn't exist")
        else:
            flash("Please enter your username and password")

        conn.commit()
        conn.close()
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/Questionaire', methods=('GET', 'POST'))
def mobile_msk_questionaire():
    """
    The only real URL of the application. When the user calls it with a GET request it displays the questionnaire. Then
    when the user fills it out and sends back the answers to the questions via a post request, the answers are used to
    diagnose the user.
    """
    questions, answers = model.Get_Questions_And_Answers()  # Gets the questions and possible answers that will be used
    # To diagnose the patient.
    if request.method == 'POST':  # If the user has already filled out the questionnaire
        symptom_data = [] #  To store answers by patient
        for q in questions:  # For each question q, each iteration q is a different question
            answers[q] = request.form.get(q)  # Get the answer to the question q
            symptom_data.append(answers[q])  # Adds answer by patients into array
        diagnosis_URL = model.diagnose(questions, answers)  # Gets the diagnosis based on the answers to the questions
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        db = sqlite3.connect('backpain.db', check_same_thread=False) # Connect to database
        cursor = db.cursor()     
        cursor.execute('''
        INSERT INTO symptoms (datetime_column, symptom1, symptom2, symptom3, symptom4)
        VALUES (?, ?, ?, ?, ?)''', (today, symptom_data[0], symptom_data[1], symptom_data[2], symptom_data[3]))
        db.commit() # Inserts symptoms of the patient into database
        db.close()
        return render_template('diagnosis.html', questions=questions, answers=answers, diagnosis=diagnosis_URL)
    terms_conditions_url = url_for('temp_placeholder')  # Sets the URL for the terms and conditions
    return render_template('questionaire.html', questions=questions, answers=answers,
                           terms_conditions_url=terms_conditions_url)  # Display the questionnaire if
    # it has not been displayed yet


@app.route('/Progress')
def progress():
    # Query the symptom data from the database
    plt.switch_backend('Agg') # To avoid crashing the server while plotting the graph
    db = sqlite3.connect('backpain.db', check_same_thread=False) # Connect to database
    cursor = db.cursor()  
    # Query the Oswestry data from the database
    cursor.execute('SELECT * FROM (SELECT datetime_column, score1, score2, score3, score4, score5, score6, score7, score8, score9, score10 FROM oswentry_individual ORDER BY datetime_column DESC LIMIT 6) ORDER BY datetime_column ASC')
    # also too include: WHERE username = ?     - session['username']
    oswentry_rows = cursor.fetchall() # Fetches Oswestry data

    # Query the Oswestry total data from the database
    cursor.execute('SELECT * FROM (SELECT datetime_column, score FROM oswentry_total ORDER BY datetime_column DESC LIMIT 6) ORDER BY datetime_column ASC')
    # also too include: WHERE username = ?     - session['username']
    oswentry_total = cursor.fetchall() # Fetches Oswestry data
    db.close()
    # Prepare the Oswestry individual data for plotting
    oswentry_individual_data = {
        'Date': [row[0] for row in oswentry_rows],
        'Score1': [row[1] for row in oswentry_rows],
        'Score2': [row[2] for row in oswentry_rows],
        'Score3': [row[3] for row in oswentry_rows],
        'Score4': [row[4] for row in oswentry_rows],
        'Score5': [row[5] for row in oswentry_rows],
        'Score6': [row[6] for row in oswentry_rows],
        'Score7': [row[7] for row in oswentry_rows],
        'Score8': [row[8] for row in oswentry_rows],
        'Score9': [row[9] for row in oswentry_rows],
        'Score10': [row[10] for row in oswentry_rows]
    }
    oswentry_individual_df = pd.DataFrame(oswentry_individual_data)

    # Prepare the Oswestry total data for plotting
    oswentry_total_data = {
        'Date': [row[0] for row in oswentry_total],
        'Score': [row[1] for row in oswentry_total]
    }
    oswentry_df = pd.DataFrame(oswentry_total_data)

    # Create the Oswestry graph
    plt.figure(figsize=(6, 3))
    plt.plot(oswentry_individual_df['Date'], oswentry_individual_df['Score1'], label='Pain Intensity')
    plt.xticks(fontsize=5)
    plt.yticks(fontsize=10)
    plt.ylim(0,5) #Range of symptom severity
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Severity')
    plt.title('Progression Over Time')
    plt.grid(True, linestyle='--')
    oswentry_1 = "static/img/oswestry1.png" # Save the Oswestry graph to a file
    plt.savefig(oswentry_1, bbox_inches='tight') #to prevent cropping any part of the graph

    plt.figure(figsize=(6, 3))
    plt.plot(oswentry_individual_df['Date'], oswentry_individual_df['Score2'], label='Personal Care')
    plt.xticks(fontsize=5)
    plt.yticks(fontsize=10)
    plt.ylim(0,5) #Range of symptom severity
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Severity')
    plt.title('Progression Over Time')
    plt.grid(True, linestyle='--')
    oswentry_2 = "static/img/oswestry2.png" # Save the Oswestry graph to a file
    plt.savefig(oswentry_2, bbox_inches='tight') #to prevent cropping any part of the graph

    plt.figure(figsize=(6, 3))
    plt.plot(oswentry_individual_df['Date'], oswentry_individual_df['Score3'], label='Lifting')
    plt.xticks(fontsize=5)
    plt.yticks(fontsize=10)
    plt.ylim(0,5) #Range of symptom severity
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Severity')
    plt.title('Progression Over Time')
    plt.grid(True, linestyle='--')
    oswentry_3 = "static/img/oswestry3.png" # Save the Oswestry graph to a file
    plt.savefig(oswentry_3, bbox_inches='tight') #to prevent cropping any part of the graph

    plt.figure(figsize=(6, 3))
    plt.plot(oswentry_individual_df['Date'], oswentry_individual_df['Score4'], label='Walking')
    plt.xticks(fontsize=5)
    plt.yticks(fontsize=10)
    plt.ylim(0,5) #Range of symptom severity
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Severity')
    plt.title('Progression Over Time')
    plt.grid(True, linestyle='--')
    oswentry_4 = "static/img/oswestry4.png" # Save the Oswestry graph to a file
    plt.savefig(oswentry_4, bbox_inches='tight') #to prevent cropping any part of the graph

    plt.figure(figsize=(6, 3))
    plt.plot(oswentry_individual_df['Date'], oswentry_individual_df['Score5'], label='Sitting')
    plt.xticks(fontsize=5)
    plt.yticks(fontsize=10)
    plt.ylim(0,5) #Range of symptom severity
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Severity')
    plt.title('Progression Over Time')
    plt.grid(True, linestyle='--')
    oswentry_5 = "static/img/oswestry5.png" # Save the Oswestry graph to a file
    plt.savefig(oswentry_5, bbox_inches='tight') #to prevent cropping any part of the graph

    plt.figure(figsize=(6, 3))
    plt.plot(oswentry_individual_df['Date'], oswentry_individual_df['Score6'], label='Standing')
    plt.xticks(fontsize=5)
    plt.yticks(fontsize=10)
    plt.ylim(0,5) #Range of symptom severity
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Severity')
    plt.title('Progression Over Time')
    plt.grid(True, linestyle='--')
    oswentry_6 = "static/img/oswestry6.png" # Save the Oswestry graph to a file
    plt.savefig(oswentry_6, bbox_inches='tight') #to prevent cropping any part of the graph

    plt.figure(figsize=(6, 3))
    plt.plot(oswentry_individual_df['Date'], oswentry_individual_df['Score7'], label='Sleeping')
    plt.xticks(fontsize=5)
    plt.yticks(fontsize=10)
    plt.ylim(0,5) #Range of symptom severity
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Severity')
    plt.title('Progression Over Time')
    plt.grid(True, linestyle='--')
    oswentry_7 = "static/img/oswestry7.png" # Save the Oswestry graph to a file
    plt.savefig(oswentry_7, bbox_inches='tight') #to prevent cropping any part of the graph

    plt.figure(figsize=(6, 3))
    plt.plot(oswentry_individual_df['Date'], oswentry_individual_df['Score8'], label='Social Life')
    plt.xticks(fontsize=5)
    plt.yticks(fontsize=10)
    plt.ylim(0,5) #Range of symptom severity
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Severity')
    plt.title('Progression Over Time')
    plt.grid(True, linestyle='--')
    oswentry_8 = "static/img/oswestry8.png" # Save the Oswestry graph to a file
    plt.savefig(oswentry_8, bbox_inches='tight') #to prevent cropping any part of the graph

    plt.figure(figsize=(6, 3))
    plt.plot(oswentry_individual_df['Date'], oswentry_individual_df['Score9'], label='Traveling')
    plt.xticks(fontsize=5)
    plt.yticks(fontsize=10)
    plt.ylim(0,5) #Range of symptom severity
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Severity')
    plt.title('Progression Over Time')
    plt.grid(True, linestyle='--')
    oswentry_9 = "static/img/oswestry9.png" # Save the Oswestry graph to a file
    plt.savefig(oswentry_9, bbox_inches='tight') #to prevent cropping any part of the graph

    plt.figure(figsize=(6, 3))
    plt.plot(oswentry_individual_df['Date'], oswentry_individual_df['Score10'], label='Employment/Homemaking')
    plt.xticks(fontsize=5)
    plt.yticks(fontsize=10)
    plt.ylim(0,5) #Range of symptom severity
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Severity')
    plt.title('Progression Over Time')
    plt.grid(True, linestyle='--')
    oswentry_10 = "static/img/oswestry10.png" # Save the Oswestry graph to a file
    plt.savefig(oswentry_10, bbox_inches='tight') #to prevent cropping any part of the graph

    plt.figure(figsize=(10, 5))
    plt.plot(oswentry_df['Date'], oswentry_df['Score'], label='Disability score')
    ax=plt.subplot()
    plt.xticks(fontsize=5)
    plt.yticks(fontsize=10)
    plt.ylim(0,50) #Range of symptom severity
    ax.set_yticks((0, 5, 10, 15, 20, 25, 30, 35, 40, 50))
    ax.set_yticklabels(("No disability", "Mild disability", "10", "Moderate disability", "20", 
                        "Severe disability", "30", "Completely disabled", "40", "50"))
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Disability Severity')
    plt.title('Progression Over Time')
    plt.grid(True, linestyle='--')
    oswentry_all = "static/img/oswestry.png" # Save the Oswestry graph to a file
    plt.savefig(oswentry_all, bbox_inches='tight') #to prevent cropping any part of the graph

    return render_template('Progress.html', oswentry_1=oswentry_1, oswentry_2=oswentry_2,oswentry_3=oswentry_3,
                            oswentry_4=oswentry_4, oswentry_5=oswentry_5, oswentry_6=oswentry_6, oswentry_7=oswentry_7,
                            oswentry_8=oswentry_8, oswentry_9=oswentry_9, oswentry_10=oswentry_10, oswentry_all=oswentry_all)  


@app.route('/OSWENTRY_Back_Pain')
def OSWENTRY_Low_Back_Pain_Questionaire():
    """

    """
    questions = model.get_OSWENTRY_Questionnaire()
    post_URL = url_for('OSWENTRY_Low_Back_Pain_Questionaire_evaluation')
    return render_template('OSWENTRY_questionnaire.html', questions=questions, post_URL=post_URL)

@app.route('/diagnosis')
def diagnosis_information():
    """

    """
    questions = model.get_diagnosis()
    post_URL = url_for('diagnosis_information')
    return render_template('diagnosis.html', questions=questions, post_URL=post_URL)

@app.route("/Acute_Backpain")
def Acute_Backpain():

    return render_template("Acute.html")

@app.route("/Subacute_Backpain")
def Subacute_Backpain():
    return render_template("Subacute.html")

@app.route("/Chronic_Backpain")
def Chronic_Backpain():
    return render_template("Chronic.html")

@app.route("/Upper_Backpain")
def Upper_Backpain():
    return render_template("Upper.html")

@app.route("/Middle_Backpain")
def Middle_Backpain():
    return render_template("Middle.html")


@app.route("/Lower_Backpain")
def Lower_Backpain():
    return render_template("Lower.html")


@app.route('/OSWENTRY_Back_Pain', methods=['POST'])
def OSWENTRY_Low_Back_Pain_Questionaire_evaluation():
    score, symptoms_data = model.score_OSWENTRY(request.form)
    disability = model.get_disability_level_from_score(score)
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO oswentry_individual (datetime_column, score1, score2, score3, score4, score5, score6, score7, score8, score9, score10) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (today, symptoms_data[0], symptoms_data[1], symptoms_data[2], symptoms_data[3], symptoms_data[4],
                    symptoms_data[5], symptoms_data[6], symptoms_data[7], symptoms_data[8], symptoms_data[9]))
    db.commit()
    cursor.execute("INSERT INTO oswentry_total (datetime_column, score) VALUES (?, ?)",
                   (today, score))
    db.commit()
    db.close()
    return render_template('OSWENTRY_Results.html', score=score, disability=disability)


@app.route('/temp_placeholder', methods=('GET', 'POST'))
def temp_placeholder():
    return 'Temporary Placeholder'


if __name__ == '__main__':
    app.run()
# I wonder if we need to designate the run env. ex. (debug=True, host='0.0.0.0')???
