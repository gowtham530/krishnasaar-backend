from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to KrishnaSaar Chatbot API!"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    
    response = {
        "text_response": f"You asked: {question}",
        "audio_url": ""
    }
    return jsonify(response)
