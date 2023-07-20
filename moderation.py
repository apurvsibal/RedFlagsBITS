import openai

openai.api_key ='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'
def get_completion_from_messages(messages, 
                                 model="gpt-3.5-turbo", 
                                 temperature=0, 
                                 max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message["content"]

def ChatModeration(messages):

    response = openai.Moderation.create(
        input=messages
    )
    for category in response["results"][0]['category_scores'] :
        if response["results"][0]['category_scores'][category] > 0.01:
            return True
    
title = "I want to rape Angelina"
if ChatModeration("""{title}"""):
    print("Please keep title in accordance with community guidlines")