from django.shortcuts import render
from lxml import etree
import os

textClasses = ['apple',\
               'games',\
               'notebook',\
               'nvidia',\
               'OS',\
               'other_news',\
               'processor',\
               'smartphone',\
               'super_computer',]
textClassesRus = ['Эпл',\
                  'Игры',\
                  'Ноутбуки',\
                  'Нвидия',\
                  'ОС',\
                  'Другие_новости',\
                  'Процессоры',\
                  'Смартфоны',\
                  'Супер_компьютеры',]
textClassesList = []
for index in range(len(textClasses)):
    textClassesList.append({"eng": textClasses[index],\
                            "rus": textClassesRus[index]})

def main(request):
    newsCount = 0
    for textClass in textClasses:
        newsFiles = os.listdir("News//data//" + textClass + "//")
        newsCount = newsCount + len(newsFiles)
    
    return render(request, "NewsMain.html",\
                  context={"textClasses": textClassesList, "newsCount": newsCount})

def section(request, className):
    textClass = textClassesList[textClasses.index(className)]

    newsFiles = os.listdir("News//data//" + className + "//")
    news = []
    for newsFile in newsFiles:
        tree = etree.parse("News//data//" + className + "//" + newsFile)
        news.append({"title": tree.xpath('//title')[0].text, "name": newsFile})

    return render(request, "NewsSection.html",\
                  context={"textClass": textClass, "news": news})

def news(request, className, newsFileName):
    tree = etree.parse("News//data//" + className + "//" + newsFileName)
    return render(request, "News.html",\
                  context={"title": tree.xpath('//title')[0].text,\
                           "text": tree.xpath('//text')[0].text})

