from flask import Flask, render_template, request, jsonify
from Ai.ai import diagnose, fill

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chatbot', methods=['GET'])
def query():
    prompt = request.args.get('prompt')
    response = diagnose(prompt)
    return jsonify(response)

@app.route('/chatbot', methods=['POST'])
def train():
    data = request.json
    diagnosis = data.get('diagnosis')
    symptoms = data.get('symptoms')
    fill(diagnosis, symptoms)

if __name__ == '__main__':
    app.run(debug=True)