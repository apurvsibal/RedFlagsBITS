import csv
import requests
import os
import uuid
import json
from dotenv import load_dotenv
load_dotenv()
import csv

key = os.environ['KEY']
endpoint = os.environ['ENDPOINT']
location = os.environ['LOCATION']
def translate_text(original_text , lang):
    path = '/translate?api-version=3.0'
    target_language_parameter = '&to=' + lang
    constructed_url = endpoint + path + target_language_parameter
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{'text': original_text}]

    # Make the call using post
    translator_request = requests.post(
        constructed_url, headers=headers, json=body)
    
    # Retrieve the JSON response
    translator_response = translator_request.json()
    print(translator_response)
    print('....................................')
    
    # Retrieve the translation
    translated_text = translator_response[0]['translations'][0]['text']

    return translated_text



def csvTranslate(file):
    languages = ['ar','es','fr','hi','zh']
    for lang in languages:
        #files = ['Moblie_MSK_Red_Flags.csv','OSWESTRY_pain.csv','QuestionProfiles.csv']
        output_file = 'locales/' + lang + "/"+  file
        input_file = 'locales/en/' + file
        with open(input_file, 'r') as csv_input, open(output_file, 'w', newline='') as csv_output:
            reader = csv.reader(csv_input)
            writer = csv.writer(csv_output)
            for row in reader:
                translated_row = [translate_text(cell,lang) for cell in row]
                writer.writerow(translated_row)
            