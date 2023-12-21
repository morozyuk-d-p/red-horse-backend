#!/usr/bin/env python3
# Main
import os

# Flask
from flask import Flask, abort, request, jsonify

# YaGPT
from langchain.chat_models.yandex import ChatYandexGPT

# PGVector
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores.pgvector import PGVector
from langchain.embeddings import HuggingFaceEmbeddings

# Templates
import random
from langchain.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

print("Loading variables from environment...")
YANDEX_API_KEY = os.environ.get('YANDEX_API_KEY')
YANDEX_FOLDER_ID = os.environ.get('YANDEX_FOLDER_ID')
CONNECTION_STRING = os.environ.get('CONNECTION_STRING')

# Connecting to YandexGPT
print("Starting YaGPT connector...")
llm = ChatYandexGPT(api_key=YANDEX_API_KEY, folder_id=YANDEX_FOLDER_ID)

# Loading data to PGVector and creating a retriever
print("Loading embeddings model...")
embeddings = HuggingFaceEmbeddings(model_name='paraphrase-multilingual-MiniLM-L12-v2')

print("Loading data from CSV...")
loader = CSVLoader(file_path='db.csv', csv_args={
    'delimiter': ';',
    'quotechar': '"'
})
data = loader.load()

print("Initializing PostgreSQL DB...")
db = PGVector.from_documents(
    embedding=embeddings,
    documents=data,
    collection_name='red_horse',
    connection_string=CONNECTION_STRING,
    pre_delete_collection=True
)

retriever = db.as_retriever()

# Creating a main template
print("Loading template...")
template_horse = '''Ты - конь Тидон, голосовой ассистент на основе искусственного интеллекта, рассказывающий о туристической привлекательности Ростовской области.
Твой характер темпераментный, но при этом весёлый и дружелюбный, любишь шутить.

Ограничения:
- Общайся естественно, как будто ты рассказываешь это в устной речи.
- Поддерживай дружелюбный и шутливый стиль.
- Отвечай лаконично, информативно и уместно.
- Ограничь длину ответа до одной строки.
- Избегай разметки Markdown, маркированных и нумерованных списков.
- НЕ ОБСУЖДАЙ ЧТО-ТО КРОМЕ РОСТОВСКОЙ ОБЛАСТИ. Если разговор ушёл на отвлеченную тему - не отвечай на вопрос, а предложи вернуться к обсуждению Ростовской области.

Ответь на вопрос, применяя ТОЛЬКО следующие данные: {context}.

Запрос пользователя: {query}
'''

prompt_horse = ChatPromptTemplate.from_template(template_horse)

def pick_most_relevant(docs):
  return docs[0]

def format_document(doc):
  return doc.page_content[doc.page_content.find('answer: ') + 8:]

def split_answers(doc):
  return doc.split('; ')

horse_chain = (
    {
        'context': retriever | pick_most_relevant | format_document | split_answers | random.choice,
        'query': RunnablePassthrough(),
    }
    | prompt_horse
    | llm
    | StrOutputParser()
)

# Exposing function to network
print("Starting Flask app...")
print("-" * 80)
app = Flask(__name__)

@app.route('/invoke', methods=['POST'])
def invoke():
    if not request.json or not 'query' in request.json:
       abort(400)
    output = horse_chain.invoke(request.json['query'])
    print("-" * 80)
    return jsonify({
       "response": output
    })

if __name__ == '__main__':
    app.run(debug=False)