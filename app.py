import flask
from flask import request, jsonify
from quote import getonequote
import json
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route('/getonequote')

#get data in body
def get_one_quote():
  question = request.json['question']
  quote = getonequote(question)

  #convert string to json
  return json.loads(quote)

#handle all exceptions
@app.errorhandler(Exception)
def handle_exception(e):
  return jsonify(error=str(e)), 500

#handle all errors
@app.errorhandler(404)
def page_not_found(e):
  return jsonify(error=str(e)), 404



if __name__ == '__main__':
  app.run(debug=True)
