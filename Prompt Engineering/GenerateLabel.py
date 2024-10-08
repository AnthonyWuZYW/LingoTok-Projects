import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import time
    
genai.configure(api_key="AIzaSyBJKGrrwQsqtwGLi5nFCVCYeXJDSqXtARE")
model = genai.GenerativeModel("gemini-1.5-flash")


for i in range(1, 20):
    path = "./Video_Finished/" + str(i) + "/"
    filename = str(i) + "_English"
    file = open(path + filename + ".srt", "r")
    lines = file.readlines()
    file.close()
    lines = [i for i in lines if i[:-1]]
    lines = ''.join(lines)

    prompt = '''What is the tag category the video based on the caption summary  without explaining
                
                Use this JSON schema:

                {"Category": [str， str, str], 
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
            break
        except:
            print("Error")
            time.sleep(1)

    print(response.text)