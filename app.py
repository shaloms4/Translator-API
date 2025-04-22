from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("API_KEY"))

@app.route("/manual-answer", methods=["POST"])
def manual_answer():
    try:
        data = request.get_json()
        input = data.get("input")  

        if not input:
            return jsonify({"error": "Missing input sentence"}), 400

        prompt = f"""
You are a professional translator. Your job is to help speakers of various languages communicate in English during travel.
Translate the following sentence to English, then provide a pronunciation of the English translation using the original language's letters.

Input: {input}

Your response format should be:

1. Translation: <English translation>
2. Pronunciation: <English sentence written phonetically in the original language's letters>

Example:

Input: እባኮትን ወደ መንገድ መነሻ ቦታ እንዴት ማሄድ እችላለሁ?
1. Translation: How can I get to the departure gate?
2. Pronunciation: ሃው ካን አይ ጌት ቱ ዘ ዲፓርቸር ጌት?

Example for Turkish input:
Input: İstanbul'a nasıl gidebilirim?
1. Translation: How can I get to Istanbul?
2. Pronunciation: Haav ken ay get tü İstanbul?

Rules for pronunciation:
- Use Turkish letters (e.g., İ, ş, ü) where applicable.
- Mimic Turkish phonetic patterns (e.g., 'how' as 'Haav', 'can' as 'ken', 'to' as 'tü').
- Ensure 'Istanbul' is written as 'İstanbul' with Turkish characters.
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        reply = response.choices[0].message.content
        return jsonify({
            "ai_reply": reply
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)
