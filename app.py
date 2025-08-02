from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Replace this with your actual Together AI key
TOGETHER_API_KEY = "tgp_v1_2pRyRXB_U7Dcow3nzf4ghmdZu8zGyZrhxF7SaQxxh3U"

# DeepSeek model endpoint and parameters
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
TOGETHER_MODEL = "deepseek-chat"

@app.route("/")
def home():
    return "Welcome to KrishnaSaar Chatbot API with DeepSeek!"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_question = data.get("question", "")

    if not user_question:
        return jsonify({"error": "No question provided."}), 400

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": TOGETHER_MODEL,
        "messages": [
            {"role": "system", "content": "You are Lord Krishna explaining answers from the Mahabharata in a wise and kind way."},
            {"role": "user", "content": user_question}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(TOGETHER_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        # Extract reply from DeepSeek
        answer = result["choices"][0]["message"]["content"]

        return jsonify({
            "text_response": answer,
            "audio_url": ""  # We will fill this later with voice output
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
