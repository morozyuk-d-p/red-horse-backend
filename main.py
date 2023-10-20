#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import AnyStr
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer


def assistant(question: AnyStr):
    question = question.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    stemmer = SnowballStemmer("russian")
    question=tokenizer.tokenize(question)


    WordArray = []
    for word in question:
        WordArray.append(stemmer.stem(word).lower())
    if "рост" in WordArray:
        WordArray = ['ростов' if x == "рост" else x for x in WordArray]


    helloKeyWords=['кон', "привет", "здравств"]
    goodByeKeyWords = ['пок', "проща", "забуд"]

    response = ''

    if any (helloWord in WordArray for helloWord in helloKeyWords):
        response+="Здравствуйте! Я конь Василий, ваш гид по достопримечательностям Ростовской области. Задайте мне вопросы об интересующей вас достопримечательности, и, если я знаю о ней, то поведаю вам! Для завершения разговора скажите пока"
        return response

    if any(goodByeKeyWord in WordArray for goodByeKeyWord in goodByeKeyWords):
        response+=("До свидания, рад был помочь!")
        return response

    if 'достопримечательн' in WordArray:
        response+= "Вот некоторые из достопримечательностей Ростовской Области, о которых я могу рассказать Археологический музей-заповедник Танаис, Вознесенский войсковой кафедральный собор в Новочеркасске, памятник Тачанка Ростовчанка, лавка Чеховых в Таганроге, Алексеевские ворота и Новочеркасский музей истории Донского казачества"
    elif 'танаис' in WordArray:
        response+= 'Древний город основанный греками выходцами из Боспорского царства. Процетал в промежутке от первой четверти третьего века до нашей эры  до середны пятого века нашей эры. Является прекрасным памятником древней архитектуры.'
    elif 'вознесенск' in WordArray or 'войсков' in WordArray:
        response+='Это великий храм, открывшийся в тысяча девятьсот пятом году. Собор долгострой, его возведение началось в тысяча восемьсот одиннадцатом году. Расположен в центре Новочеркасска на вершине холма. В хорошую погоду золоченые купола, инкрустированные горным хрусталем кресты видны за десятки километров'
    elif 'тачанк' in WordArray or 'ростовчанк' in WordArray:
        response+='Год открытия этого мемориала – тысяча девятьсот семьдесят седьмой год. Год выбран не случайный – к 60-летию революции. Расположен при южном въезде в Ростов-на-Дону, посвящен бойцам Первой конной Буденного, бившихся здесь с деникинской Добровольческой армией. Изначально гипсовый, покрыт медными листами. Реставрировался в две тысячи девятом году с полным сохранением деталей. Пятнадцатиметровый монумент стал одной из визиток города, с ним связан ряд местных традиций.'
    elif 'чехов' in WordArray:
        response+='Год основания этого музея – тысяча девятьсот семьдесят пятый год. В период проживания семьи Чехова здесь на первом этаже размещалась лавка бакалеи, на втором – жилые помещения. Ряд произведений Антона Павловича создан по мотивам рассказов посетителей магазинчика, услышанных им в юном возрасте. Здесь представлен период отрочества писателя, восстановлен интерьер, собраны несколько семейных фотографий и личных вещей семейства Чеховых.'
    elif 'алексеевск' in WordArray:
        response+= 'Главные крепостные ворота Азова постройки семнадцатого века, откопанные и отреставрированные в тысяча девятьсот тридцать пятом году. С частью земляного вала и рва это единственная сохранившаяся часть укреплений бывшей турецкой крепости. Алексеевские ворота неоднократно перестраивались, сейчас сохранен их каменный вариант тысяча восемьсот пятого года, кропотливо восстановленный по уцелевшим чертежам времен их возведения.'
    elif 'казачеств' in WordArray:
        response+= 'Год основания – тысяча восемьсот восемьдесят шестой. В коллекции сто пятьдесят тысяч экспонатов, причем посвященных не только казачеству. В экспозициях – ископаемые древности, оружие, доспехи, монеты, чучела местной фауны, собрание фарфора, легендарный донской камыш, высотой под потолок этажа здания – более восьми метров. Разделен на тематические залы, включая огромную коллекцию предметов царских времен, революции и Второй мировой.'
    else:
        response+= "К сожалению, я не могу ответить на ваш вопрос. Или я вас не так понял, или вы спрашиваете меня о том, о чем я не знаю, не могли бы вы повторить вопрос, если он относится к теме достопримечательностей Ростовской области"
    return response

if __name__ == "__main__":
    print("RED HORSE v0.0.2 alpha INTERACTIVE MODE")
    print("-" * 80)
    while True:
        question = input("> ")
        response = assistant(question)
        print(f"< {response}")