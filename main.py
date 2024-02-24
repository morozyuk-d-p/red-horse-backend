#!/usr/bin/env python3
# Main
import os

# FastAPI + LangServe
from fastapi import FastAPI
from langserve import add_routes

# PGVector
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores.pgvector import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings

# Answers formatting
import random
from langchain_core.runnables import RunnableLambda

print(
    """NEUROHORSE, rev. 2024.02.09
(c) Morozyuk Daniil, 2024

[INIT BEGIN]"""
)

# Loading values from environment variables
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
    search_kwargs={"score_threshold": 0.3, "k": 1},
)

# Exposing function to network
print("Starting LangServe...")
print("[INIT DONE]")
print("-" * 80)
app = FastAPI(
    title="NEUROHORSE", version="1.0", description="Red Horse Tidon backend server"
)


# Chain definition
def debug(arg):
    if len(arg) != 0:
        for index, item in enumerate(arg):
            print(f"[DB[{index}] DATA]\n{item.page_content}\n[DB[{index}] DATA END]")
            print(f"[DB[{index}] META] {item.metadata}")
    return arg


def pickRandom(documents):
    if len(documents) != 0:
        document = documents[0]
        choice = random.choice(
            document.page_content[document.page_content.find("answer: ") + 8 :].split(
                "; "
            )
        )
        print(f"[PICK] {choice}")
        return choice


def removeLastSemicolon(string: str):
    if string[-1] == ";":
        return string[0 : len(string) - 1]
    else:
        return string


def route(ctx):
    if len(ctx) != 0:
        debug(ctx)
        return removeLastSemicolon(pickRandom(ctx))
    else:
        print("[DB] No answer found, falling back to error chain...")
        return "Извините, я не могу ответить на этот вопрос."


chain = retriever | RunnableLambda(route)

add_routes(app, chain, path="/horse")

# Launch web server on executing script
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
