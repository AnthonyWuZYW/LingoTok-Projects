import google.generativeai as genai

text = "i am a turtle"

genai.configure(api_key="AIzaSyBJKGrrwQsqtwGLi5nFCVCYeXJDSqXtARE")
model = genai.GenerativeModel("gemini-1.5-pro")
prompt = """Create one question for new English learner based on the summary 
            and four capitalized lettered options, 
            then give correct answer in one capitalized letter in Answer: , make sure there is no asterisk

            Use this JSON schema:

            {'Question': str, 
             'Options': list[str]
             'Answer': str
             }"""

result = model.generate_content([text, prompt])
print(result.text)