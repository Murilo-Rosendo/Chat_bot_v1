from flask import Flask, jsonify, render_template, request

from src.chatbot import MuriloBot
from src.database import init_database, save_chat_history


app = Flask(__name__)

init_database()
bot = MuriloBot()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/perguntar", methods=["POST"])
def perguntar():
    texto_usuario = request.form.get("texto", "").strip()

    if not texto_usuario:
        return jsonify({"resposta": "Digite uma mensagem para eu conseguir ajudar."}), 400

    resultado = bot.responder(texto_usuario)

    save_chat_history(
        pergunta_usuario=texto_usuario,
        categoria_detectada=resultado["categoria"],
        resposta_bot=resultado["resposta"],
        confianca=resultado["confianca"],
    )

    return jsonify(resultado)


if __name__ == "__main__":
    print("\n" + "=" * 52)
    print("Murilo Bot iniciado.")
    print("Acesse: http://127.0.0.1:5000")
    print("=" * 52 + "\n")
    app.run(debug=True, use_reloader=False)
