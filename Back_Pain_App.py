"""
Purpose:
    API for the application.
"""

from flask import Flask, render_template, request, url_for, redirect
# From flask import send_file, send_from_directory, abort
# Import SQL
import _sqlite3
from datetime import date
import matplotlib.pyplot as plt
import pandas as pd
# Import io
import os
# From datetime import date
import model

app = Flask(__name__)
path = str(os.path.dirname(os.path.abspath(__file__)))
path = path.replace('\\', '/')
app.config['files'] = path + '/temp/'
db = _sqlite3.connect('backpain.db', check_same_thread=False) # Connect to database
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS symptoms(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE,
    symptom1 TEXT,
    symptom2 TEXT,
    symptom3 TEXT,
    symptom4 TEXT);''')
    # add more tables if necessary
db.commit() # Create "symptoms" table if not already created


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
                           more_information=more_information, next_question_number=question_number+1)


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
        today = date.today().isoformat()
        cursor.execute('''
        INSERT INTO symptoms (date, symptom1, symptom2, symptom3, symptom4)
        VALUES (?, ?, ?, ?, ?)''', (today, symptom_data[0], symptom_data[1], symptom_data[2], symptom_data[3]))
        db.commit() # Inserts symptoms of the patient into database
        return render_template('Diagnosis.html', questions=questions, answers=answers, diagnosis=diagnosis_URL)
    terms_conditions_url = url_for('temp_placeholder')  # Sets the URL for the terms and conditions
    return render_template('questionaire.html', questions=questions, answers=answers,
                           terms_conditions_url=terms_conditions_url)  # Display the questionnaire if
    # it has not been displayed yet


@app.route('/Progress')
def progress():
    # Query the symptom data from the database
    plt.switch_backend('Agg') # To avoid crashing the server while plotting the graph
    cursor.execute('SELECT date, symptom1, symptom2, symptom3, symptom4 FROM symptoms')
    rows = cursor.fetchall() # Fetches all data returned from above query

    # Prepare the data for plotting
    data = {
        'Date': [row[0] for row in rows],
        'Symptom1': [row[1] for row in rows],
        'Symptom2': [row[2] for row in rows],
        'Symptom3': [row[3] for row in rows],
        'Symptom4': [row[4] for row in rows]
        # Add more fields for other symptoms
    }
    df = pd.DataFrame(data)

    # Create the charts or graphs
    plt.figure(figsize=(6, 4)) # To change size and ratio of graph
    plt.plot(df['Date'], df['Symptom1'], label='Where is your pain the worst?')
    plt.plot(df['Date'], df['Symptom2'], label='Is your pain constant?')
    plt.plot(df['Date'], df['Symptom3'], label='Does your pain get worse when bending?')
    plt.plot(df['Date'], df['Symptom4'], label='Does your pain get worse when sitting or standing?')
    # Add more plots for other symptoms

    plt.xlabel('Date')
    plt.ylabel('Symptom Severity')
    plt.title('Symptom Progression Over Time')
    plt.grid(True, linestyle='--') #to include gridlines, easier to read
    # plt.yticks(fontsize=4) #for chaning font of y-axis labels
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0) # To get the legend out of the graph
    #plt.legend() # To let the legend be in the plot at the best place
    # Save the plot to a file
    plot_filename="RedFlagsBITS/static/img/progress_plot.png"
    plt.savefig(plot_filename, bbox_inches = 'tight') #to prevent cropping any part of the graph
    return render_template('Progress.html', plot_filename="/static/img/progress_plot.png")


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
