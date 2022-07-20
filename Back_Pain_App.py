"""
Purpose:
    API for the application.
"""

from flask import Flask, render_template, request, url_for, redirect
# from flask import send_file, send_from_directory, abort
# import io
import os
# from datetime import date
import model

app = Flask(__name__)
path = str(os.path.dirname(os.path.abspath(__file__)))
path = path.replace('\\', '/')
app.config['files'] = path + '/temp/'


@app.route('/', methods=('GET', 'POST'))  # Route and accepted Methods
@app.route('/index', methods=('GET', 'POST'))
def index():
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
    return render_template('questionaire.html', questions=questions, answers=answers)  # Display the questionnaire if
    # it has not been displayed yet


if __name__ == '__main__':
    app.run()
# I wonder if we need to designate the run env. ex. (debug=True, host='0.0.0.0')???
