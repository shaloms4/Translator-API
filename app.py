from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import os
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("API_KEY"))

@app.route("/manual-answer", methods=["POST"])
def manual_answer():
    try:
        data = request.get_json()
        input_sentence = data.get("input")

        if not input_sentence:
            return jsonify({"error": "Missing input sentence"}), 400

        prompt = f"""
You are a professional translator. Your job is to help speakers of various languages communicate in English during travel.
Translate the following sentence to English, then provide a pronunciation of the English translation using the original language's letters.

Input: {input_sentence}

Your response format should be:

1. Translation: <English translation>
2. Pronunciation: <English sentence written phonetically in the original language's letters>

Important:
- DO NOT repeat or include the original sentence in your response.
- Just return the translation and pronunciation.

Example:

Input: እባኮትን ወደ መንገድ መነሻ ቦታ እንዴት ማሄድ እችላለሁ?
Translation: How can I get to the departure gate?
Pronunciation: ሃው ካን አይ ጌት ቱ ዘ ዲፓርቸር ጌት?

Example for Turkish input:
Input: İstanbul'a nasıl gidebilirim?
Translation: How can I get to Istanbul?
Pronunciation: Haav ken ay get tü İstanbul?
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        reply = response.choices[0].message.content

        # Simple parsing
        translation = "Translation unavailable."
        pronunciation = "Pronunciation unavailable."
        
        for line in reply.split('\n'):
            line = line.strip()
            if line.startswith("1. Translation:"):
                translation = line.replace("1. Translation:", "").strip()
            elif line.startswith("2. Pronunciation:"):
                pronunciation = line.replace("2. Pronunciation:", "").strip()

        parsed_response = {
            "translation": translation,
            "pronunciation": pronunciation
        }

        return Response(
            json.dumps(parsed_response, ensure_ascii=False),
            content_type='application/json; charset=utf-8'
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)
