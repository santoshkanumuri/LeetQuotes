import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
import requests
from bs4 import BeautifulSoup as bs

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

def getonequote(slug_name):
  data = {"operationName":"questionData","variables":{"titleSlug":slug_name},"query":"query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n"}
  r = requests.post('https://leetcode.com/graphql', json = data).json()
  soup = bs(r['data']['question']['content'], 'html.parser')
  question= soup.text
  print(question)
  chat_session = connect_ai()
  question = f'''Given the following problem description from LeetCode: {question}, provide two things in a JSON format:
  Analyze the problem given, what is the main requirement for output and understand the requirements and then build an optimal solution that can handle edge cases, and large data entry for this question. now form solution steps to solve
  this question. then from solution steps generate a concise, simple or motivational or love or life or quirky quote-like hint that guides the programmer towards solution of the problem that describes the key idea to solve the problem.
A step-by-step breakdown of the solution approach in a clear and simple manner.
structure your output clearly in a json format and should contain two fields: 'quote' and 'solution'. Ensure the hint offers key insights into the problem-solving approach, while the solution provides clear steps for implementation'''
  response = chat_session.send_message(question)
  return response.text
