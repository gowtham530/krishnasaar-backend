from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ✅ Replace with your actual Together API key
TOGETHER_API_KEY = "tgp_v1_2pRyRXB_U7Dcow3nzf4ghmdZu8zGyZrhxF7SaQxxh3U"

# ✅ Working Together AI setup
TOGETHER_API_URL = "https://api.together.xyz/inference"
TOGETHER_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"  # Confirmed working

@app.route("/")
def home():
    return "Welcome to KrishnaSaar Chatbot API (powered by Mistral on Together.ai)"

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

        # 🔍 Print full response in logs
        print("DeepSeek raw response:", result)

        # ✅ FIX: Extract answer from choices[0].text
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