import google.generativeai as genai
import os
import json
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import time


def generateQuestion(path, filename, resultPath, model):
    file = open(path + filename + ".srt", "r")
    lines = file.readlines()
    file.close()
    lines = [i for i in lines if i[:-1]]
    lines = ''.join(lines)

    prompt = '''Create one title for new English learner based on the summary 
                then give the around 30 words summary

                Use this JSON schema:

                {"Title": str, 
                 "Summary": str
                }'''
    
    while True:
        try:
            response = model.generate_content([lines, "\n", prompt], 
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
                }
            )
            print(response.text)
            break
        except:
            print("Error")
            time.sleep(1)
    

    text = ''.join(response.text.splitlines()[1:-1])
    json_text = json.loads(text)
    json_object = json.dumps(json_text, indent=4)
    if not os.path.exists(resultPath):
        os.makedirs(resultPath)
    with open(resultPath + "/"+ filename + ".json", "w") as outfile:
        outfile.write(json_object)


genai.configure(api_key="AIzaSyBJKGrrwQsqtwGLi5nFCVCYeXJDSqXtARE")
model = genai.GenerativeModel("gemini-1.5-flash")

resultFolder = "Generated Info"
start = 138
end = 210
for i in range(start, end+1):
    path = "./Video_Finished/" + str(i) + "/"
    filename = str(i) + "_English"
    generateQuestion(path, filename, resultFolder, model)
    



