from flask import Flask, jsonify, request, render_template
import google.generativeai as genai
import json
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import time
import pandas as pd
import os
import requests

app = Flask(__name__)
genai.configure(api_key="AIzaSyBJKGrrwQsqtwGLi5nFCVCYeXJDSqXtARE")
model = genai.GenerativeModel("gemini-1.5-flash")
url = "https://logininfo-ba28.restdb.io/rest/login"
headers = { 'content-type': "application/json",
            'x-apikey': "9aa1e93a97e3045896d07a1177ac2f72ffa3c",
            'cache-control': "no-cache"}

@app.route('/')
def hello():
    return render_template('/home.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'] 

        return 'Login successful!'

    return render_template('/login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'] 
        confirmPassword = request.form['confirmPassword'] 

        # Validate password match
        if password != confirmPassword:
            return jsonify({'error': 'Passwords do not match.'})

        # Save data to CSV
        data = {'email': email, 'password': password}
        data = json.dumps( data)
        requests.request("POST", url, data=data, headers=headers)

        return 'Registration successful!'
    else:
        return render_template('register.html')
    


@app.route('/get_question', methods = ['POST'])  
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


if __name__ == '__main__':
    app.run(host = 'localhost', port = 8088, debug = True)