import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

def connect_ai():
  GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')
  genai.configure(api_key=GOOGLE_API_KEY)
  # Create the model
  generation_config = {
  "temperature": 1.5,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,

  "response_mime_type": "application/json",
  }
  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-002",
    generation_config=generation_config,
  )

  chat_session = model.start_chat(history=[])


  return chat_session

def getonequote(question):
  chat_session = connect_ai()
  question = f'''Given the following problem description from LeetCode: {question}, provide two things in a JSON format:

A concise, quirky or simple or motivational or love or life quote-like hint that guides the programmer towards solution of the problem.
A step-by-step breakdown of the solution approach in a clear and simple manner.
structure your output clearly in a json format and should contain two fields: 'quote' and 'solution'. Ensure the hint offers key insights into the problem-solving approach, while the solution provides clear steps for implementation'''
  response = chat_session.send_message(question)
  return response.text
