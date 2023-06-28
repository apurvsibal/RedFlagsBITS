"""
Purpose:
    API for the application.
"""

from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
path = str(os.path.dirname(os.path.abspath(__file__)))
path = path.replace('\\', '/')
app.config['UPLOAD_FOLDER'] = path + '/static/files'


@app.route('/', methods=('GET', 'POST'))
@app.route('/index', methods=('GET', 'POST'))
def index():
    header_1 = 'Red Flags'
    header_2 = 'For Back Pain'
    explanation = """
    Some cases of back pain can be serious, and require immediate medical attention.
    We are going to ask a few questions to understand the nature of your pain.
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
            Use the map below to see some providers.
            """
        map_link = 'https://goo.gl/maps/zKXs4iFKqaqDwfJy6'
        return render_template('immediate_care.html', header_1=header_1, explanation=explanation, map_link=map_link)
    elif not question_number:
        question_number = 1
    elif question_number > num_question:
        return redirect(url_for('mobile_msk_questionnaire'))
    question, answers, more_information = model.get_red_flag_question(question_number)
    return render_template('Red_Flags.html', header_1=header_1, question=question, answers=answers,
                           more_information=more_information, next_question_number=question_number + 1)


@app.route('/Questionnaire', methods=('GET', 'POST'))
def mobile_msk_questionnaire():
    questions, answers = model.Get_Questions_And_Answers()
    if request.method == 'POST':
        for q in questions:
            answers[q] = request.form.get(q)
        diagnosis_URL = model.diagnose(questions, answers)
        return render_template('Diagnosis.html', questions=questions, answers=answers, diagnosis=diagnosis_URL)
    terms_conditions_url = url_for('temp_placeholder')
    return render_template('questionnaire.html', questions=questions, answers=answers,
                           terms_conditions_url=terms_conditions_url)


@app.route('/OSWENTRY_Back_Pain')
def OSWENTRY_Low_Back_Pain_questionnaire():
    questions = model.get_OSWENTRY_questionnaire()
    post_URL = url_for('OSWENTRY_Low_Back_Pain_questionnaire_evaluation')
    return render_template('OSWENTRY_questionnaire.html', questions=questions, post_URL=post_URL)


@app.route('/OSWENTRY_Back_Pain', methods=['POST'])
def OSWENTRY_Low_Back_Pain_questionnaire_evaluation():
    score = model.score_OSWENTRY(request.form)
    disability = model.get_OSWENTRY_disability_level(score)
    return render_template('OSWENTRY_results.html', score=score, disability=disability)


@app.route('/static/files/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


class UploadForm(FlaskForm):
    file = FileField(validators=[FileRequired()])


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
