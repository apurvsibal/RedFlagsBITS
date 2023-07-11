from flask import Flask, render_template, request, redirect, url_for, escape
import warnings
warnings.filterwarnings('ignore')

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.llms import AzureOpenAI
import os
from typing import Dict

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-03-15-preview"
os.environ["OPENAI_API_BASE"] = "https://openairedflags.openai.azure.com/"
os.environ["OPENAI_API_KEY"] = "41d6760e6a674dae891eef613eae5b69"

llm = AzureOpenAI(
    deployment_name="symptoms",
    model_name="text-davinci-002",
)

app = Flask(__name__)

backpain_template = """ using symptoms from symptoms checker genrate a paragraph including information about symptom, possible diagnosis,causes,risk factors and treatment.
give a informational paragraph.

{input}"""

redflag_template = """generate a list of redflags (in medical terms) based on symptoms from symptom checker and put '.' after each line.\
make sure 2 '.' are never together.\

Here is a question:
{input}"""

opqrst_template = """for a particular type of symptom\
generate a OPQRST questions to answer and put '?' after each question of acronym.\
make sure 2 '?' are never together.\

Here is a question:
{input}"""

vindicate_template = """for a particular type of symptom\
generate a VINDICATE questions to answer and put '?' after each question of acronym.\
make sure 2 '?' are never together.\

Here is a question:
{input}"""

prompt_template = backpain_template
prompt = ChatPromptTemplate.from_template(template=prompt_template)
chain = LLMChain(llm=llm, prompt=prompt)

redflag_prompt_template = redflag_template
redflag_prompt = ChatPromptTemplate.from_template(template=redflag_prompt_template)
redflag_chain = LLMChain(llm=llm, prompt=redflag_prompt)

opqrst_prompt_template = opqrst_template
opqrst_prompt = ChatPromptTemplate.from_template(template=opqrst_prompt_template)
opqrst_chain = LLMChain(llm=llm, prompt=opqrst_prompt)

vindicate_prompt_template = vindicate_template
vindicate_prompt = ChatPromptTemplate.from_template(template=vindicate_prompt_template)
vindicate_chain = LLMChain(llm=llm, prompt=vindicate_prompt)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/symptom-checker', methods=['GET', 'POST'])
def symptom_checker():
    if request.method == 'POST':
        selected_symptoms = request.form.get('symptoms')
        input_text = " ".join(selected_symptoms.split(","))
        response = chain.run(input_text)
        diagnosis_info = response

        # Redirect to OPQRST page with selected symptoms as a query parameter
        return render_template('result.html', selected_symptoms=selected_symptoms, diagnosis_info=diagnosis_info)

    return render_template('symptom_checker.html')

@app.route('/redflag', methods=['GET', 'POST'])
def redflag():
    if request.method == 'POST':
        selected_symptoms = request.form.get('symptoms')
        input_text = selected_symptoms
        response = redflag_chain.run(input_text)
        red_quest = response

        questions = []
        for line in response.split("\n"):
            if "?" in line:
                questions.append(line[:line.find("?")])
            else:
                questions.append(line)

        # Redirect to OPQRST page with selected symptoms as a query parameter
        return render_template('redflag.html', selected_symptoms=selected_symptoms, red_quest=questions)

    return render_template('results.html')


@app.route('/opqrst', methods=['GET', 'POST'])
def opqrst():
    if request.method == 'POST':
        selected_symptoms = request.form.get('symptoms')
        input_text = selected_symptoms
        response = opqrst_chain.run(input_text)
        interview_quest = response

        questions = []
        for line in response.split("\n"):
            if "?" in line:
                questions.append(line[:line.find("?")])
            else:
                questions.append(line)

        # Redirect to OPQRST page with selected symptoms as a query parameter
        return render_template('opqrst.html', selected_symptoms=selected_symptoms, interview_quest=questions)

    return render_template('results.html')

@app.route('/vindicate', methods=['GET', 'POST'])
def vindicate():
    if request.method == 'POST':
        selected_symptoms = request.form.get('symptoms')
        input_text = selected_symptoms
        response = vindicate_chain.run(input_text)
        vind_quest = response

        questions = []
        for line in response.split("\n"):
            if "?" in line:
                questions.append(line[:line.find("?")])
            else:
                questions.append(line)

        # Redirect to OPQRST page with selected symptoms as a query parameter
        return render_template('vindicate.html', selected_symptoms=selected_symptoms, vind_quest=questions)

    return render_template('results.html')



if __name__ == '__main__':
    app.run(debug=True)
