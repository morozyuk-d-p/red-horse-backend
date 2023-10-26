#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import random
import sqlite3
from typing import AnyStr
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
import pandas as pd
from loger import logger


def bd_create():
    """
    Создает базу данных с exel файла
    :return: ничего не возвращает
    """
    conn = sqlite3.connect('horse_database.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS my_table (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
        '''
    )
    cursor.close()
    # Загрузка данных из Excel
    df = pd.read_excel('bd.xlsx')

    df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)
    print(df)
    # Загрузка данных в базу данных SQLite
    df.to_sql('my_table', conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()
    logger.debug("База данных создана")


def delete_bd():
    if os.path.exists('horse_database.db'):
        os.remove('horse_database.db')
        logger.debug("База данных удалена.")
    else:
        logger.debug("База данных не существует.")


def remove_empty_elements(input_list):
    processed_list = [element for element in input_list if element.strip() != '']
    return processed_list


def find_answer(keyword):
    """

    :param keyword: Ключевое слова
    :return: возвращает ответ
    """
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect("horse_database.db")
    cursor = conn.cursor()

    query = "SELECT answer FROM my_table WHERE LOWER(keywords) LIKE '%' || LOWER(?) || '%'"
    cursor.execute(query, (keyword.lower(),))

    # Получаем результат запроса
    result = cursor.fetchone()

    # Закрываем соединение с базой данных
    conn.close()
    if result:
        list = remove_empty_elements(result[0].split(";"))
        return list[random.randint(0, len(list) - 1)]  # Возвращаем найденный ответ
    else:
        return None
    print(result)
    return result


def assistant(question: AnyStr):
    logger.debug('вопрос (question): [' + question + "]")
    question = question.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    stemmer = SnowballStemmer("russian")
    question = tokenizer.tokenize(question)

    WordArray = []
    for word in question:
        WordArray.append(stemmer.stem(word).lower())
    if "рост" in WordArray:
        WordArray = ['ростов' if x == "рост" else x for x in WordArray]

    helloKeyWords = ['кон', "привет", "здравств"]
    goodByeKeyWords = ['пок', "проща", "забуд"]

    print(WordArray)
    response = ''

    if any(helloWord in WordArray for helloWord in helloKeyWords):
        response += "Здравствуйте! Я конь Василий, ваш гид по достопримечательностям Ростовской области. Задайте мне вопросы об интересующей вас достопримечательности, и, если я знаю о ней, то поведаю вам! Для завершения разговора скажите пока"
        return response

    if any(goodByeKeyWord in WordArray for goodByeKeyWord in goodByeKeyWords):
        response += ("До свидания, рад был помочь!")
        return response

    result = next((find_answer(word) for word in WordArray if find_answer(word)), None)
    return result


if __name__ == "__main__":
    delete_bd()
    bd_create()
    print("RED HORSE v0.0.2 alpha INTERACTIVE MODE")
    logger.debug("RED HORSE v0.0.2 alpha INTERACTIVE MODE")
    print("-" * 80)
    while True:
        question = input("> ")
        response = assistant(question)
        print(f"< {response}")
        logger.debug('ответ (response): [' + response + ']')
