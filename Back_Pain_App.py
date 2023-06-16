"""
Purpose:
    API for the application.
"""
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, session
import re
# from flask import send_file, send_from_directory, abort
# import io
import os
from datetime import date, timedelta, datetime
import model
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

secret_key = secrets.token_hex(16)
app = Flask(__name__)
app.secret_key = secret_key

path = str(os.path.dirname(os.path.abspath(__file__)))
path = path.replace('\\', '/')
app.config['files'] = path + '/temp/'


@app.route('/', methods=('GET', 'POST'))  # Route and accepted Methods
@app.route('/index', methods=('GET', 'POST'))
def index():
    """

    """
    header_1 = 'Red Flags'
    header_2 = 'For Back Pain'
    explanation = """
    Some cases of back pain can be serious, and require immediate medical attention.
    We are going to ask a few question to understand the nature of your pain.
    """
    return render_template('index.html', header_1=header_1, header_2=header_2, explanation=explanation)


@app.route('/red_flags', methods=('GET', 'POST'))
@app.route('/red_flags/<int:question_number>', methods=('GET', 'POST'))
def red_flags_questionnaire(question_number: int = 0):
    num_question = 3
    header_1 = 'Is your back pain associated with any of the following?'
    if question_number and request.args.get('answer') == 'Yes':
        header_1 = 'You need immediate care'
        explanation = """
            You answered 'Yes' to a question indicating you could be in need of emergency care. 
            Use the map below to see some providers
            """
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
        for q in questions:  # For each question q, each iteration q is a different question
            answers[q] = request.form.get(q)  # Get the answer to the question q
        diagnosis_URL = model.diagnose(questions, answers)  # Gets the diagnosis based on the answers to the questions
        return render_template('Diagnosis.html', questions=questions, answers=answers, diagnosis=diagnosis_URL)
    terms_conditions_url = url_for('temp_placeholder')  # Sets the URL for the terms and conditions
    return render_template('questionaire.html', questions=questions, answers=answers,
                           terms_conditions_url=terms_conditions_url)  # Display the questionnaire if
    # it has not been displayed yet


@app.route('/OSWENTRY_Back_Pain')
def OSWENTRY_Low_Back_Pain_Questionaire():
    """

    """
    questions = model.get_OSWENTRY_Questionnaire()
    post_URL = url_for('OSWENTRY_Low_Back_Pain_Questionaire_evaluation')
    return render_template('OSWENTRY_questionnaire.html', questions=questions, post_URL=post_URL)


@app.route('/OSWENTRY_Back_Pain', methods=['POST'])
def OSWENTRY_Low_Back_Pain_Questionaire_evaluation():
    """

    """
    score = model.score_OSWENTRY(request.form)
    disability = model.get_disability_level_from_score(score)
    return render_template('OSWENTRY_Results.html', score=score, disability=disability)


@app.route('/temp_placeholder', methods=('GET', 'POST'))
def temp_placeholder():
    return 'Temporary Placeholder'


if __name__ == '__main__':
    app.run()
# I wonder if we need to designate the run env. ex. (debug=True, host='0.0.0.0')???
