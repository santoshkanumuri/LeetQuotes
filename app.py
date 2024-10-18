from flask import Flask, request, jsonify
from quote import getonequote
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/getonequote', methods=['POST'])
def get_one_quote():
    try:
        # Get data from the request body
        question = request.json.get('question')

        if not question:
            return jsonify(error="Missing 'question' in request body"), 400

        # Call the getonequote function and assume it returns a JSON string
        quote = getonequote(question)

        # If quote is already a JSON string, just return it using jsonify
        return jsonify(json.loads(quote))

    except Exception as e:
        return jsonify(error=str(e)), 500

# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error="Endpoint not found"), 404

if __name__ == '__main__':
    app.run(debug=True)
