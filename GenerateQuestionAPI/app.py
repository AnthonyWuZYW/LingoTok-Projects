from flask import Flask, request
import google.generativeai as genai
import os
import json
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import time

app = Flask(__name__)
genai.configure(api_key="AIzaSyBJKGrrwQsqtwGLi5nFCVCYeXJDSqXtARE")
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/')
def hello():
    return 'No file received'

@app.route('/', methods = ['POST'])  
def generateQuestions():
    content = request.files['file'].read().decode("utf-8")
    prompt = '''Create one question for new English learner based on the summary 
                and four capitalized lettered options, 
                then give correct answer in one capitalized letter in Answer: , make sure there is no asterisk

                Use this JSON schema:

                {"Question": str, 
                 "Options": [ "A." str, "B." str, "C." str, "D." str],
                 "Answer": str
                }'''
    
    while True:
        try:
            response = model.generate_content([content, "\n", prompt], 
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
                }
            )
            break
        except:
            print("Failed to get a response, retrying...")
            time.sleep(1)
    
    text = ''.join(response.text.splitlines()[1:-1])
    json_text = json.loads(text)
    json_object = json.dumps(json_text, indent=4)
    
    return json_object
