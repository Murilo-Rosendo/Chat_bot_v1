import random

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

from src.database import load_responses, load_training_data


class MuriloBot:
    def __init__(self):
        self.vectorizer = CountVectorizer(strip_accents="unicode", lowercase=True)
        self.model = MultinomialNB()
        self.responses = {}
        self.ready = False
        self.train()

    def train(self):
        frases, categorias = load_training_data()
        self.responses = load_responses()

        if not frases or not categorias:
            self.ready = False
            return

        training_matrix = self.vectorizer.fit_transform(frases)
        self.model.fit(training_matrix, categorias)
        self.ready = True

    def responder(self, texto_usuario):
        if not self.ready:
            return {
                "resposta": "Ainda não tenho dados suficientes para responder.",
                "categoria": "erro",
                "confianca": 0,
            }

        input_matrix = self.vectorizer.transform([texto_usuario])
        probabilities = self.model.predict_proba(input_matrix)[0]
        confidence = float(max(probabilities))
        category = str(self.model.predict(input_matrix)[0])

        if confidence < 0.18:
            return {
                "resposta": "Não entendi totalmente sua dúvida. Pode escrever de outro jeito?",
                "categoria": "nao_entendido",
                "confianca": round(confidence, 4),
            }

        options = self.responses.get(
            category,
            ["Entendi sua solicitação, mas ainda não tenho uma resposta cadastrada para ela."],
        )

        return {
            "resposta": random.choice(options),
            "categoria": category,
            "confianca": round(confidence, 4),
        }
