from django.shortcuts import render
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import pickle
import re

# Инициализация классификатора и словаря слов
classifier = pickle.load(open("Classifier/Hi_News_Model.dat", 'rb'))
Hi_News_Dictionary = []
file = open("Classifier/Hi_News_Dictionary.txt", encoding='utf-8')
for line in file:
    Hi_News_Dictionary.append(line[:-1])
file.close()

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

def makeVector(text):
    vector = [0] * len(Hi_News_Dictionary)
    for word in text.split():
        normalizedWord = re.sub(r'[.,\/#!\?$%\^&\*;:{}=_`~()]', '', word.lower()).strip()
        if normalizedWord:
            if normalizedWord in Hi_News_Dictionary:
                index = Hi_News_Dictionary.index(normalizedWord)
                vector[index] = vector[index] + 1
    return np.array([vector], int)

def getTextClass(text):
    result = classifier.predict(makeVector(text))
    return textClassesRus[int(result[0]) - 1]


def classify(request):
    if request.method == "POST":
        text = request.POST.get("text")

        textClass = getTextClass(text)
        
        return render(request, "ClassifyResult.html",\
                      context={"textClass": textClass})
    else:
        return render(request, "ClassifyForm.html")

