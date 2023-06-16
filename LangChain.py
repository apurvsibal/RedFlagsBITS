import os
import openai
os.environ["OPENAI_API_KEY"] = "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"
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain
from langchain.agents import tool
from langchain.agents.agent_toolkits import create_python_agent
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from langchain.tools.python.tool import PythonREPLTool
from langchain.python import PythonREPL
from langchain.chat_models import ChatOpenAI

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, 
    )
    return response.choices[0].message["content"]



# Define the Agent class
class PatientAgent:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.symptoms = []

    def add_symptom(self, symptom):
        self.symptoms.append(symptom)

    def get_context(self):
        context = f"The patient's name is {self.name} and their age is {self.age}."
        if self.symptoms:
            context += f" They are experiencing {', '.join(self.symptoms)} in terms of back pain."
        return context

# Define the email generation function using the Agent
def generate_email(agent,email):
    context = agent.get_context()

    email_prompt = f""" You are an AI service bot and you are writing a email to the patient\
    after diagnosing them based on the symtoms described in {context}. Write the mail in a professional\
    manner and do not provide any specific details about the diagnosis. Always contain an assuring tone in the\
    email. Sign the email by Red_Flags. End the email properly. Send the email to {email}
    """

    agent_message = {
        "role": "user",
        "content": email_prompt
    }

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a doctor."},
            agent_message
        ],
        
    )

    return response.choices[0].message['content']

# Create an instance of the PatientAgent and add symptoms
patient = PatientAgent("John Doe", 45)
patient.add_symptom("lower back pain")
patient.add_symptom("muscle stiffness")

# Generate the email based on patient information
email=input("Enter your email")
generated_email = generate_email(patient,email)

# Print the generated email
print(generated_email)


