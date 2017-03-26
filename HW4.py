from nltk.corpus import wordnet
from nltk.wsd import lesk

#1
for i in wordnet.synsets('plant'): 
    print(i, ': ', i.definition())

print ("\n=============================================\n")
#2
def1 = wordnet.synset('plant.n.01') #Завод
print("Завод:", def1.definition())
def2 = wordnet.synset('plant.n.02') #Растение
print("Растение:", def2.definition())

print ("\n=============================================\n")

#3
context1 = {def1.definition():"allow the plant to rest with no food and little water for about six weeks"} #BNC
context2 = {def2.definition():"the company has also achieved a grade A accreditation from the plant evaluation committee of the National Association of Catering Butchers"}
context1.update(context2)
contexts = context1
for i in contexts:
    if lesk(contexts[i], 'plant').definition() == i:
        print ("Алгоритм Леска сработал для контекста ", contexts[i])
    else:
        print ("Алгоритм Леска не сработал для контекста ", contexts[i])

print ("\n=============================================\n")

#4
print("Гиперонимы для контекста ", def1.definition(), ":" )
for i in def1.hypernyms():
    print(i)
print("Гиперонимы для контекста ", def2.definition(), ":" )
for i in def2.hypernyms():
    print(i)

print ("\n=============================================\n")

#5

def distance(definition, lex, s_type="path"):
    res_noneable = []
    for i in wordnet.synsets(lex):
        if s_type == "path":
            res_noneable.append(definition.path_similarity(i))
        elif s_type == "wup":
            res_noneable.append(definition.wup_similarity(i))
        elif s_type == "lch":
            res_noneable.append(definition.lch_similarity(i))
    res = [] 
    for i in res_noneable:
        if i:
            res.append(i)      
    if res:
        return min(res)
    else:
        return "Error"
        
print('"завод" & industry')
m_lex = 'industry'
res = distance(def1, m_lex)
print ("Минимальное раccтояние:", res)

print('"завод" & leaf')
m_lex = 'leaf'
res = distance(def1, m_lex)
print ("Минимальное раccтояние:", res)

print('"растение" & industry')
m_lex = 'industry'
res = distance(def1, m_lex)
print ("Минимальное раccтояние:", res)

print('"растение" & leaf')
m_lex = 'leaf'
res = distance(def1, m_lex)
print ("Минимальное раccтояние:", res)

print ("\n=============================================\n")

#6

print("Расстояние между plant & rattlesnake; Метод: Path:", distance(def2, "rattlesnake"))
print("Расстояние между organism & whole; Метод: Path:", distance(wordnet.synset("organism.n.01"), "whole"))

print("Расстояние между plant & rattlesnake; Метод: Wu Palmer:", distance(def2, 'rattlesnake', "wup"))
print("Расстояние между organism & whole; Метод: Wu Palmer:", distance(wordnet.synset("organism.n.01"), "whole", "wup"))

#По первому алгоритму расстояние меньше. Но мне кажется, что WuP лучше отражает положение дел.  

