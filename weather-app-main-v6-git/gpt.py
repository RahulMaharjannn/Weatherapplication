import openai
from dotenv import load_dotenv
from pprint import pprint
import requests
import os

load_dotenv()

#API_KEY = open("OpenAIKey.txt", "r").read()

template="Take this weather json data and give a roughly 40 word weather report, ignore complicated data like latitude and longitude. Make it short and simple: "
userTemplateFront="Take this weather json data and give a roughly 50 word weather report, include metrics like: "
userTemplateBack=". DO NOT INCLUDE metrics like: "

def get_gpt_text(question='Echo what I say: No question was provided to GPT API!'):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {"role": "user", "content": question}
    ])
    
    return (response['choices'][0]['message']['content'])


#print(get_gpt_text('How big is an apple?'))
