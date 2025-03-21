from flask import Flask, request, jsonify, render_template
import replicate

app = Flask(__name__)

# Configure ta clé API Replicate
REPLICATE_API_TOKEN = "r8_1xhjcM4KDLDjoogw1tJT3mIEhxqBlGc2XFRzt"
replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

def query_llama(prompt):
    """
    Envoie une requête à un modèle LLaMA via Replicate.
    """
    try:
        print(f"Envoi du prompt à Replicate : {prompt}")
        output = replicate_client.run(
            "meta/llama-2-7b-chat",  # Modèle LLaMA-2-7B
            input={"prompt": prompt, "max_tokens": 150}
        )
        print(f"Réponse reçue de Replicate : {output}")
        return output
    except Exception as e:
        print(f"Erreur lors de la requête à Replicate : {e}")
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

    # Utilise Replicate pour interagir avec LLaMA
    response = query_llama(user_input)

    if "error" in response:
        return jsonify({"error": response["error"]}), 500

    # Transforme la liste en une seule chaîne de caractères
    if isinstance(response, list):
        response = "".join(response)

    return jsonify({"response": response})

if __name__ == "__main__":
    # Configure pour le Raspberry Pi
    app.run(host="0.0.0.0", port=6060, debug=True)
