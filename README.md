# Murilo Bot

Murilo Bot é um chatbot web feito com Python, Flask, scikit-learn e SQLite. Ele responde dúvidas simples sobre saldo, extrato, Pix, cartão, pagamentos, empréstimos, segurança e atendimento humano.

## Tecnologias

- Python
- Flask
- SQLite
- scikit-learn
- HTML, CSS e JavaScript

## Estrutura

```txt
Murilo_Bot/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   ├── perguntas.csv
│   └── respostas.json
├── instance/
│   └── .gitkeep
├── scripts/
│   └── init_db.py
├── src/
│   ├── __init__.py
│   ├── chatbot.py
│   └── database.py
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── chat.js
└── templates/
    └── index.html
```

## Como rodar

Crie e ative um ambiente virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie o banco SQLite:

```bash
python scripts/init_db.py
```

Inicie o servidor:

```bash
python app.py
```

Abra no navegador:

```txt
http://127.0.0.1:5000
```

## Banco de dados

O banco é criado em `instance/chatbot.db` a partir dos arquivos:

- `data/perguntas.csv`
- `data/respostas.json`

O arquivo `.db` fica fora do Git pelo `.gitignore`, porque ele é gerado localmente e também guarda o histórico das conversas.

## Exemplos de perguntas

```txt
oi
como vejo meu saldo?
quero fazer um pix
perdi meu cartao
limite
bloquear
quero ver meu extrato
esqueci minha senha
quero falar com atendente
```
