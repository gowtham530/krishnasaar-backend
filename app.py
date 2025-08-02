from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ✅ Your Together API key here
TOGETHER_API_KEY = "tgp_v1_2pRyRXB_U7Dcow3nzf4ghmdZu8zGyZrhxF7SaQxxh3U"

# ✅ Correct Together.ai API
TOGETHER_API_URL = "https://api.together.xyz/inference"
TOGETHER_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"

@app.route("/")
def home():
    return "Welcome to KrishnaSaar Chatbot API (Powered by Mistral on Together.ai)"

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
        "prompt": f"[INST] {user_question} [/INST]",
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9,
        "repetition_penalty": 1.1
    }

    try:
        response = requests.post(TOGETHER_API_URL, headers=headers, json=payload)
        result = response.json()

        # Debugging help — shows full API result in Render logs
        print("DeepSeek raw response:", result)

        # ✅ Safe and correct format for Mistral model
        if "choices" in result and len(result["choices"]) > 0:
            answer = result["choices"][0]["text"].strip()
        else:
            answer = "Sorry, the model didn’t return a proper response."

        return jsonify({
            "text_response": answer,
            "audio_url": ""
        })

    except Exception as e:
        print("Exception:", str(e))
        return jsonify({"error": "Server error occurred."}), 500
