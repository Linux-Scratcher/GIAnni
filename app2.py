from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Remplace par l'URL de l'API LLaMA
LLaMA_API_URL = "https://api.llama-api.com/"

# Remplace par ta clé API LLaMA
API_KEY = "67fb7c09-2cd4-4fed-abc6-1f6f26640097"

def query_llama(prompt):
    """
    Envoie une requête à l'API LLaMA et retourne la réponse.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 150
    }

    try:
        print(f"Envoi de la requête à l'API LLaMA avec le prompt : {prompt}")
        response = requests.post(LLaMA_API_URL, headers=headers, json=data)
        response.raise_for_status()  # Lève une exception si le statut HTTP est une erreur
        print(f"Réponse reçue de l'API : {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête à l'API LLaMA : {e}")
        return {"error": str(e)}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """
    Gère les messages de l'utilisateur et retourne la réponse de LLaMA.
    """
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "Aucun message fourni"}), 400

    # Pour tester sans l'API, utilise une réponse fixe
    # response = {"choices": [{"text": "Ceci est une réponse fixe."}]}

    # Utilise l'API LLaMA
    response = query_llama(user_input)

    if "error" in response:
        return jsonify({"error": response["error"]}), 500

    # Assure-toi que la réponse contient bien le champ attendu
    if "choices" not in response or not response["choices"]:
        return jsonify({"error": "Réponse de l'API invalide"}), 500

    return jsonify(response)

if __name__ == "__main__":
    # Configure pour le Raspberry Pi
    app.run(host="0.0.0.0", port=6868, debug=True)
