#!/usr/bin/env python3
# Main
import random
import os
import base64

# FastAPI + LangServe
from fastapi import FastAPI
from langserve import add_routes

# Chain toolkit
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

# GigaChat
from langchain_community.chat_models.gigachat import GigaChat

# PGVector
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores.pgvector import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings

print(
    """NEUROHORSE, rev. 2024.02.09
(c) Morozyuk Daniil, 2024

[INIT BEGIN]"""
)

# Loading values from environment variables
print("Loading variables from environment...")
CONNECTION_STRING = os.environ.get("CONNECTION_STRING")
GIGACHAT_CLIENT_ID = os.environ.get("GIGACHAT_CLIENT_ID")
GIGACHAT_CLIENT_SECRET = os.environ.get("GIGACHAT_CLIENT_SECRET")

# Establish link with GigaChat
print("Establishing link with GigaChat API...")
giga = GigaChat(
    credentials=base64.b64encode(
        f"{GIGACHAT_CLIENT_ID}:{GIGACHAT_CLIENT_SECRET}".encode()
    ).decode(),
    verify_ssl_certs=False,
)


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


@app.get("/")
def onVisitMain():
    return "Игого! Я конь Тидон!"


# Chain definition
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Представь, что ты конь Тидон - харизматичный, темпераментный, весёлый и шутливый гид по Ростовской области.
            Ты используешь базу данных в качестве справки для ответа пользователям.
            Правила взаимодействия с пользователями:
            - Составляй предложения кратко, но доходчиво, чтобы ответы подходили для устного прослушивания.
            - Ограничь длину ответа до 2-3 предложений.
            - Не используй разметку Markdown и спецсимволы.
            """,
        ),
        (
            "human",
            """
            Мой вопрос: {question}
            Информация из базы данных: {context}
            """,
        ),
    ]
)


def logRAG(arg):
    if len(arg) != 0:
        for index, item in enumerate(arg):
            print(f"[DB[{index}] DATA]\n{item.page_content}\n[DB[{index}] DATA END]")
            print(f"[DB[{index}] META] {item.metadata}")
    return arg

def logLLM(arg):
    print(f"[LLM] {arg}")
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
        logRAG(ctx)
        return removeLastSemicolon(pickRandom(ctx))
    else:
        print("[DB] No answer found, falling back to error chain...")
        return "Извините, я не могу ответить на этот вопрос."


rag_chain = (
    {
        "question": RunnablePassthrough(),
        "context": retriever | RunnableLambda(route),
    }
    | prompt
    | giga
    | StrOutputParser()
    | logLLM
)

db_chain = retriever | RunnableLambda(route)

add_routes(app, giga, path="/giga")
add_routes(app, rag_chain, path="/rag", input_type=str)
add_routes(app, db_chain, path="/db")

# Launch web server on executing script
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
