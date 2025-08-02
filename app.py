from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ✅ Your Together AI key goes here
TOGETHER_API_KEY = "tgp_v1_2pRyRXB_U7Dcow3nzf4ghmdZu8zGyZrhxF7SaQxxh3U"

# ✅ Correct API and model for DeepSeek
TOGETHER_API_URL = "https://api.together.xyz/inference"
TOGETHER_MODEL = "deepseek-ai/deepseek-chat"  # or use deepseek-coder-6.7b-instruct

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
        "prompt": f"User: {user_question}\nAssistant:",
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9,
        "repetition_penalty": 1.1
    }

    try:
        response = requests.post(TOGETHER_API_URL, headers=headers, json=payload)
        result = response.json()

        # Check if output exists
        if "output" in result:
            answer = result["output"]
        else:
            print("DeepSeek error response:", result)
            answer = "Sorry, the model didn’t return a proper response."

        return jsonify({
            "text_response": answer,
            "audio_url": ""  # TTS will be added later
        })

    except Exception as e:
        print("Exception:", str(e))
        return jsonify({"error": "Server error occurred."}), 500
