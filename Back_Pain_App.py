from flask import Flask, render_template, request, url_for, jsonify
import os
import model
from datetime import datetime

app = Flask(__name__)
path = str(os.path.dirname(os.path.abspath(__file__)))
path = path.replace('\\', '/')
app.config['files'] = path + '/temp/'


@app.route('/', methods=('GET', 'POST'))
@app.route('/index', methods=('GET', 'POST'))
def index():
    """
    Renders the index.html template with back pain information.
    """
    header_1 = 'Red Flags'
    header_2 = 'For Back Pain'
    explanation = """
    Some cases of back pain can be serious and require immediate medical attention.
    We are going to ask a few questions to understand the nature of your pain.
    """
    return render_template('index.html', header_1=header_1, header_2=header_2, explanation=explanation)


@app.route('/red_flags', methods=('GET', 'POST'))
@app.route('/red_flags/<int:question_number>', methods=('GET', 'POST'))
def red_flags_questionnaire(question_number: int = 0):
    """
    Handles the red flags questionnaire, displays questions and collects answers.
    """
    num_question = 3
    header_1 = 'Is your back pain associated with any of the following?'
    if question_number and request.args.get('answer') == 'Yes':
        header_1 = 'You need immediate care'
        explanation = """
            You answered 'Yes' to a question indicating you could be in need of emergency care.
            Use the map below to see some providers.
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


@app.route('/questionaire', methods=('GET', 'POST'))
def mobile_msk_questionaire():
    """
    Displays the questionnaire and handles the form submission.
    """
    questions, answers = model.Get_Questions_And_Answers()
    if request.method == 'POST':
        for q in questions:
            answers[q] = request.form.get(q)
        diagnosis_URL = model.diagnose(questions, answers)
        return render_template('Diagnosis.html', questions=questions, answers=answers, diagnosis=diagnosis_URL)
    terms_conditions_url = url_for('temp_placeholder')
    return render_template('questionaire.html', questions=questions, answers=answers,
                           terms_conditions_url=terms_conditions_url)


@app.route('/OSWENTRY_Back_Pain')
def OSWENTRY_Low_Back_Pain_Questionaire():
    """
    Renders the OSWENTRY questionnaire template.
    """
    questions = model.get_OSWENTRY_Questionnaire()
    post_URL = url_for('OSWENTRY_Low_Back_Pain_Questionaire_evaluation')
    return render_template('OSWENTRY_questionnaire.html', questions=questions, post_URL=post_URL)


@app.route('/OSWENTRY_Back_Pain', methods=['POST'])
def OSWENTRY_Low_Back_Pain_Questionaire_evaluation():
    """
    Evaluates the OSWENTRY questionnaire and renders the results template.
    """
    score = model.score_OSWENTRY(request.form)
    disability = model.get_disability_level_from_score(score)
    return render_template('OSWENTRY_Results.html', score=score, disability=disability)


@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        selected_date = request.form.get('selected_date')
        selected_time = request.form.get('selected_time')
        # Process the selected_date and selected_time as needed
        # Implement appointment scheduling logic here
        # Return the appropriate response
        return jsonify(success=True, message='Appointment scheduled successfully.')

    return render_template('appointment.html')


if __name__ == '__main__':
    app.run()
