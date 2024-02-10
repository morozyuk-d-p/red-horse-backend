#!/usr/bin/env python3
# Main
import os

# Flask
from flask import Flask, abort, request, jsonify

# PGVector
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores.pgvector import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings

# Answers formatting
import random
from langchain_core.runnables import RunnableLambda

print("""NEUROHORSE, rev. 2024.02.09
(c) Morozyuk Daniil, 2024

[INIT BEGIN]""")

print("Loading variables from environment...")
CONNECTION_STRING = os.environ.get("CONNECTION_STRING")

# Loading data to PGVector and creating a retriever
print("Loading embeddings model...")
embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")

print("Loading data from CSV...")
loader = CSVLoader(file_path="db.csv", csv_args={"delimiter": ";", "quotechar": '"'})
data = loader.load()

print("Initializing PostgreSQL DB...")
db = PGVector.from_documents(
    embedding=embeddings,
    documents=data,
    collection_name="red_horse",
    connection_string=CONNECTION_STRING,
    pre_delete_collection=True,
)

retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "score_threshold": 0.3,
        "k": 1
    },
)

def debug(arg):
    if len(arg) != 0:
        for index, item in enumerate(arg):
            print(f'[DB[{index}] DATA]\n{item.page_content}\n[DB[{index}] DATA END]')
            print(f'[DB[{index}] META] {item.metadata}')
    return arg

def pickRandom(documents):
    if len(documents) != 0:
        document = documents[0]
        choice = random.choice(document.page_content[document.page_content.find('answer: ') + 8:].split('; '))
        print(f"[PICK] {choice}")
        return choice

def route(ctx):
    if len(ctx) != 0:
        debug(ctx)
        return pickRandom(ctx)
    else:
        print("[DB] No answer found, falling back to error chain...")
        return "Извините, я не могу ответить на этот вопрос."

chain = retriever | RunnableLambda(route)

# Exposing function to network
print("Starting Flask app...")
print("[INIT DONE]")
print("-" * 80)
app = Flask(__name__)


@app.route("/invoke", methods=["POST"])
def invoke():
    if not request.json or not "query" in request.json:
        abort(400)
    print("-" * 80)
    print(f'[USER] {request.json["query"]}')
    output = chain.invoke(request.json["query"])
    print(f'[AI] {output}')
    return jsonify({"response": output})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
