import re, math
import numpy as np
from collections import Counter
from matplotlib import pyplot as plt

with open('anna.txt', encoding='utf-8') as f:
    anna = f.read()
f.close()
with open('sonets.txt', encoding='utf-8') as f:
    sonets = f.read()
f.close()    

anna_sentences = re.split(r'(?:[.]\s*){3}|[.?!]', anna)
sonet_sentences = re.split(r'(?:[.]\s*){3}|[.?!]', sonets)
    
get_words = re.compile("[А-Яа-я]*")
vowels = "ёуеыаоэяию"

def calc_parameters(collection):
    results = []
    for sents in collection:
        sent_len = 0
        different_letters = []
        sent_vowels = 0
        letters_med = []
        vowels_med = []
        words = []
        re_words = get_words.findall(sents.lower())
        for i in re_words:
            if i:
                words.append(i)
        for word in words:
            if word:
                word_vowels = 0
                for letter in word:
                    sent_len += 1
                    if letter not in different_letters:
                        different_letters.append(letter)
                    if letter in vowels:
                        sent_vowels += 1
                        word_vowels += 1
                letters_med.append(len(word))
                vowels_med.append(word_vowels)
        if sent_len > 0:
            different_letters = len(different_letters)
            letters_med = np.median(letters_med)
            vowels_med = np.median(vowels_med)
            results.append([sent_len, different_letters, sent_vowels, letters_med, vowels_med])
    
    summ_results = [0, 0, 0, 0, 0]
    for i in results:
        for j in range(5):
            summ_results[j] += i[j]
    middle_results = []
    for i in summ_results:
        middle_results.append(float(i)/float(len(results)))
    return middle_results, results

def vect_dist(a, b):
    summ = 0
    for i in range(len(a)):
        summ += (a[i] - b[i])**2
    return math.sqrt(summ)

def visual_parameters(first, second):
    features = ['Number of letters in sentence', 'Number of different letters', 'Number of vowels', 'Word length median', 'Number of vowels median']
    first = np.array(first)
    second = np.array(second)
    for i in range(5):
        for j in range(5):
            if i != j:
                print(features[i] + '+' + features[j] + ': ')
                plt.figure()
                plt.plot(first[:,i] , first[:,j], 'og', second[:,i] , second[:,j], 'ob')
                plt.show()


def classifier(collection1, collection2, test_sentences=[""]):
    first, full_first = calc_parameters(anna_sentences)
    second, full_second = calc_parameters(sonet_sentences)

    visual_parameters(full_first, full_second)
    
    index1 = 0
    index2 = 0
    for sentence in test_sentences:  
        if sentence:
            print ('"', sentence, '"')
            try:
                result = calc_parameters([sentence])
                compare1 = vect_dist(result, first)
                compare2 = vect_dist(result, second)
                if compare1 < compare2:
                    print ("First collection")
                    index1 += 1
                elif compare2 < compare1:
                    print ("Second collection")
                    index2 += 1
                else:
                    print ("Very similar to both")
                    index1 += 1
                    index2 += 1
            except:
                print ("Incorrect sentence")
        else:
            print ("Empty sentence")
    print (index1, '/', len(test_sentences), ' = ', index1/len(test_sentences))
    print (index2, '/', len(test_sentences), ' = ', index2/len(test_sentences))
classifier(anna_sentences, sonet_sentences, anna_sentences)

#Проверка классификатора на корпусе Анны Карениной.
#Он правильно определяет 8062 предложениz из 21499 (точность 37 %, что довольно плохой результат). 
#Если наоборот проверить его на сонетах, получится 1016 из 1378, точность 73%.
#Неправильно классифицированные предложения (из Анны Карениной):
# 1) Потом добрая и несколько жалкая улыбка показалась на его красивом лице
# 2) - Ну, так давай одеваться, -- обратился он к Матвею и решительно скинул халат
# Из сонетов:
# 1) У сердца с глазом - тайный договор: Они друг другу облегчают муки, Когда тебя напрасно ищет взор И сердце задыхается в разлуке
# 2) Тоскую я, лишенный равновесья, Пока стихии духа и огня Ко мне обратно не примчатся с вестью, Что друг здоров и помнит про меня








