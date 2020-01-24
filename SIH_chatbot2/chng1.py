import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
from sklearn.neural_network import MLPClassifier
import numpy
import random
import json
import pickle
from sklearn.externals import joblib 
from nltk import word_tokenize
from nltk.corpus import stopwords
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
pairs = [
    [
        'how are you',"I'm great...What can I do for you"
    ],
    [
        'hi',"Kon'nichiwa,that's hello in japanese !  How may I help"
    ],

]
with open("training.json") as file:
    data = json.load(file)

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

def chat():
    print("Start talking with the bot (type quit to stop)!")
    # print(message)
    while True:
        inp = input()
        if inp.lower() == "quit":
            break
        for i in range(len(pairs)):
            if pairs[i][0] in inp:
                break
        tokens=word_tokenize(inp)
        stop_words = set(stopwords.words('english'))
        clean_tokens = [w for w in tokens if not w in stop_words]
        query2=' '
        query2=query2.join(clean_tokens)
        # data = json.load(file)
        scor=0
        dis=""
        for i in data["intents"]:
            # print(i["patterns"])
            inpn=i["patterns"][random.randint(0,len(i["patterns"])-1)]
            # print(inp)
            tokens=word_tokenize(inpn)
            stop_words = set(stopwords.words('english'))
            clean_tokens = [w for w in tokens if not w in stop_words]
            query1=' '
            query1=query1.join(clean_tokens)
            # print(query1,query2)
            # p=sentence_similarity(query1,query2)
            p=similar(query1,query2)
            print(p)
            if p>scor:
                print(p)
                dis=i["tag"]
                scor=p
        print("you may probably have{}".format(dis))
chat()