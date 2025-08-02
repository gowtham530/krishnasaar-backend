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
    user_lang = data.get("lang", "en")  # "en", "hi", "te"

    if not user_question:
        return jsonify({"error": "No question provided."}), 400

    # Step 1: Translate input to English if needed
    def translate_to_english(text, source_lang):
        if source_lang == "en":
            return text
        try:
            response = requests.post("https://libretranslate.com/translate", json={
                "q": text,
                "source": source_lang,
                "target": "en",
                "format": "text"
            })
            return response.json()["translatedText"]
        except:
            return text

    translated_question = translate_to_english(user_question, user_lang)

    # Step 2: Send to Together AI
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": TOGETHER_MODEL,
        "prompt": f"[INST] {translated_question} [/INST]",
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9,
        "repetition_penalty": 1.1
    }

    try:
        response = requests.post(TOGETHER_API_URL, headers=headers, json=payload)
        result = response.json()
        print("Mistral response:", result)

        if "choices" in result and len(result["choices"]) > 0:
            english_answer = result["choices"][0]["text"].strip()
        else:
            english_answer = "Sorry, the model didn’t return a proper response."

        # Step 3: Translate back to user language
        def translate_from_english(text, target_lang):
            if target_lang == "en":
                return text
            try:
                response = requests.post("https://libretranslate.com/translate", json={
                    "q": text,
                    "source": "en",
                    "target": target_lang,
                    "format": "text"
                })
                return response.json()["translatedText"]
            except:
                return text

        translated_answer = translate_from_english(english_answer, user_lang)

        return jsonify({
            "text_response": translated_answer,
            "english_reference": english_answer,
            "audio_url": ""  # Voice output next
        })

    except Exception as e:
        print("Exception:", str(e))
        return jsonify({"error": "Server error occurred."}), 500
