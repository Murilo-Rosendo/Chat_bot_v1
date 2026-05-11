import csv
import json
import sqlite3
from datetime import datetime
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
INSTANCE_DIR = ROOT_DIR / "instance"
DB_PATH = INSTANCE_DIR / "chatbot.db"

PERGUNTAS_PATH = DATA_DIR / "perguntas.csv"
RESPOSTAS_PATH = DATA_DIR / "respostas.json"

CATEGORIA_DESCRICOES = {
    "saudacao": "Cumprimentos e início de atendimento.",
    "saldo": "Consultas de saldo da conta.",
    "extrato": "Consultas de extrato e movimentações.",
    "pix": "Envio, recebimento e chaves Pix.",
    "cartao": "Dúvidas sobre cartão, limite, bloqueio e segunda via.",
    "pagamento": "Pagamentos de boletos e comprovantes.",
    "emprestimo": "Simulação e contratação de empréstimos.",
    "seguranca": "Segurança, senha, fraude e acesso.",
    "atendimento_humano": "Encaminhamento para suporte humano.",
    "agradecimento": "Agradecimentos e encerramento cordial.",
    "despedida": "Finalização da conversa.",
}


def get_connection():
    INSTANCE_DIR.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def load_seed_questions():
    with PERGUNTAS_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        return [
            {
                "frase": row["frase"].strip(),
                "categoria": row["categoria"].strip(),
            }
            for row in csv.DictReader(file)
            if row.get("frase") and row.get("categoria")
        ]


def load_seed_responses():
    with RESPOSTAS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def init_database():
    questions = load_seed_questions()
    responses = load_seed_responses()

    with get_connection() as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                descricao TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS perguntas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                frase TEXT NOT NULL UNIQUE,
                categoria_id INTEGER NOT NULL,
                FOREIGN KEY (categoria_id) REFERENCES categorias(id)
            );

            CREATE TABLE IF NOT EXISTS respostas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                texto TEXT NOT NULL UNIQUE,
                categoria_id INTEGER NOT NULL,
                FOREIGN KEY (categoria_id) REFERENCES categorias(id)
            );

            CREATE TABLE IF NOT EXISTS historico_conversas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pergunta_usuario TEXT NOT NULL,
                categoria_detectada TEXT NOT NULL,
                resposta_bot TEXT NOT NULL,
                confianca REAL NOT NULL,
                data_hora TEXT NOT NULL
            );
            """
        )

        categorias = sorted(
            set([item["categoria"] for item in questions]) | set(responses.keys())
        )

        for categoria in categorias:
            conn.execute(
                "INSERT OR IGNORE INTO categorias (nome, descricao) VALUES (?, ?)",
                (
                    categoria,
                    CATEGORIA_DESCRICOES.get(categoria, "Categoria do Murilo Bot."),
                ),
            )

        categoria_ids = {
            nome: categoria_id
            for categoria_id, nome in conn.execute("SELECT id, nome FROM categorias")
        }

        conn.executemany(
            "INSERT OR IGNORE INTO perguntas (frase, categoria_id) VALUES (?, ?)",
            [
                (item["frase"], categoria_ids[item["categoria"]])
                for item in questions
                if item["categoria"] in categoria_ids
            ],
        )

        response_rows = []
        for categoria, textos in responses.items():
            categoria_id = categoria_ids.get(categoria)
            if categoria_id is None:
                continue
            response_rows.extend((texto, categoria_id) for texto in textos)

        conn.executemany(
            "INSERT OR IGNORE INTO respostas (texto, categoria_id) VALUES (?, ?)",
            response_rows,
        )


def load_training_data():
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT perguntas.frase, categorias.nome
            FROM perguntas
            JOIN categorias ON categorias.id = perguntas.categoria_id
            ORDER BY perguntas.id
            """
        ).fetchall()

    frases = [row[0] for row in rows]
    categorias = [row[1] for row in rows]
    return frases, categorias


def load_responses():
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT categorias.nome, respostas.texto
            FROM respostas
            JOIN categorias ON categorias.id = respostas.categoria_id
            ORDER BY respostas.id
            """
        ).fetchall()

    respostas = {}
    for categoria, texto in rows:
        respostas.setdefault(categoria, []).append(texto)
    return respostas


def save_chat_history(pergunta_usuario, categoria_detectada, resposta_bot, confianca):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO historico_conversas (
                pergunta_usuario,
                categoria_detectada,
                resposta_bot,
                confianca,
                data_hora
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                pergunta_usuario,
                categoria_detectada,
                resposta_bot,
                float(confianca),
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
