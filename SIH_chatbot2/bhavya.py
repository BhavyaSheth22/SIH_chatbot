import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
from sklearn.neural_network import MLPClassifier
import numpy
import random
import json
import pickle
from sklearn.externals import joblib 
from sih_chatbot.models import Patient
from flask_login import current_user

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

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)


    training = numpy.array(training)
    #print(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)
######################
######################

try:
    model = joblib.load('trained.pkl')
    print("Using pickle")
except:
    print("Using model")
    model = MLPClassifier(solver='lbfgs', random_state = 1, hidden_layer_sizes = (20,10), verbose=True)
    model.fit(training, output)
    joblib.dump(model, 'trained.pkl')

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)


def chat(message):
    print("Start talking with the bot (type quit to stop)!")
    print(message)
    # while True:
    inp = message
    # if inp.lower() == "quit":
    #     break
    # if "history" in inp:
    #     user = User.query.filter-by(email=current_user.email)
    #     message =""
    #     message = "for"+user.first_name+" "+user.last_name+"\n"
    #     message += "age:"+user.age+"\n"
    #     message += "weight:"+user.weight+"\theight"+user.height+"\n"
    #     message += "gender:"+user.gender+"\tblood group:"+blood_group+"\n"
    #     message += "conditions:"
    #     for c in user.conditions :
    #         message+= c+","
    #     message += "\nsymptoms:"
    #     for s in user.symptoms :
    #         message += s+","
    #     message += "\nprior surgeries:"+user.surgery
    #     message += "\n"+user.surgery_text
    #     message += "\nmedication:"+user.medication
    #     message += "\n"+user.medication_text
    #     message += "\nprior allergies:"+user.allergy
    #     message += "\n"+user.allergy_text
    #     return message

    # if "bmi" or "body mass index" in inp:
    #     user = User.query.filter-by(email=current_user.email)
    #     message = "your bmi is:" + user.bmi
    #     return message
        
    results = model.predict([bag_of_words(inp, words)])[0]
    results_index = numpy.argmax(results)
    tag = labels[results_index]

    for tg in data["intents"]:
        if tg['tag'] == tag:
            response = tg['response']
    print("mymy")
    return(random.choice(response))
    # return("Hiya")
