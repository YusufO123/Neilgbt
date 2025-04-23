from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

API_KEYS = {
    "123abc-neilgbt-test": "Yusuf",
    "456def-neilgbt-user": "TestKullanici"
}

openai.api_key = "senin_openai_keyin"

@app.route('/')
def index():
    return jsonify({"message": "NeilGbt API v1 hazır!"})

@app.route('/v1/chat', methods=['POST'])
def chat():
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return jsonify({"error": "API anahtarı eksik"}), 401

    user_api_key = auth.split(" ")[1]
    if user_api_key not in API_KEYS:
        return jsonify({"error": "Geçersiz API anahtarı"}), 403

    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "Mesaj eksik"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen bir yardımcı yapay zekasın."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response["choices"][0]["message"]["content"]
        return jsonify({"response": reply.strip()})
    except Exception as e:
        return jsonify({"error": "Cevap alınamadı", "detay": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
