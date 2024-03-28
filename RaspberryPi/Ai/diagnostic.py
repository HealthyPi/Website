import json
import os
from nltk.stem import WordNetLemmatizer, PorterStemmer

dirname = '/'.join(__file__.split('\\')[:-1])
lemmatizer = WordNetLemmatizer()

def loadDiagnoses() :
    with open(f'{dirname}/knowledge_base.json', 'r') as fl:
        data = json.load(fl)
        
    return data['diagnosis']

def lemmatize(sentence):
    words = []
    for word in sentence.split(' '):
        lem_order_of_importance = [
            lemmatizer.lemmatize(word, 'n'),
            lemmatizer.lemmatize(word, 'v'),
            lemmatizer.lemmatize(word, 'r'),
            lemmatizer.lemmatize(word, 'a')
        ]
        for lem_word in lem_order_of_importance:
            if lem_word != word:
                words.append(lem_word)
                break
        else:
            words.append(word)
    return ' '.join(words)

def fill(diagnosis, symptoms):
    with open(f'{dirname}/knowledge_base.json', 'r') as fl:
        data = json.load(fl)

    if diagnosis not in list(data['diagnosis'].keys()):
        data['diagnosis'][diagnosis] = {
            "symptoms" : [f"{diagnosis} is yet to be catagorized by admin."],
            "user-symptoms" : symptoms,
            "treatment" : [],
            "next-steps" : [],
            "severity" : 0,
            "rarity" : 0
        }
        with open(f"{dirname}/unknown.txt", "a") as fl:
            fl.write(f"\n{diagnosis}")

    illness = data['diagnosis'][diagnosis]
    ill_symptoms = illness['symptoms'].copy()
    ill_symptoms.extend(illness['user-symptoms'])
    lemmed = [lemmatize(symptom) for symptom in ill_symptoms]

    for symptom in symptoms:
        if lemmatize(symptom) not in lemmed:
            illness['user-symptoms'].append(symptom)
    
    with open(f'{dirname}/knowledge_base.json', 'w') as fl:
        json.dump(data, fl, indent=4)

def diagnose(prompt) :
    # if not os.path.exists(f'{dirname}/knowledge_base.json'):
    #     data = {
    #         "diagnosis" : dict()
    #     }
    #     with open(f'{dirname}/knowledge_base.json', 'w') as fl:
    #         json.dump(data, fl, indent=4)

    data = loadDiagnoses() # load trained data
    returnData = {} # response
    likeliest = 0
    likeliest_name = ''
    for diagnosis in data: # loop over all trained illness

        likelyhood = 0 # chance of having this diagnosis
        symptoms = [*data[diagnosis]['symptoms'], *data[diagnosis]['user-symptoms']]
        for symptom in symptoms:
            # remove all lexical meaning leaving only keywords
            if lemmatize(symptom) in lemmatize(prompt):
                # symptom is a match (they have a symptom of this diagnosis)
                likelyhood += 1

        # factor in how rare each disease is and
        # say that rarer diseases are less likely
        # because while covid-19 and the common cold
        # have the same symptoms, one is much more
        # likely (rarity is on a 1-10 scale)
                
        likelyhood *= 10 - data[diagnosis]['rarity']

        # if you have symptoms of the disease, add it to the return value

        if likelyhood != 0:
            returnData[diagnosis] = data[diagnosis]
            returnData[diagnosis]['chance'] = likelyhood

        if likelyhood > likeliest:
            likeliest = likelyhood
            likeliest_name = diagnosis
    
    if likeliest_name != '':
        returnData.pop(likeliest_name)
    returnData = {
        "diagnosis" : {likeliest_name: data[likeliest_name]} if likeliest_name != '' else None,
        "other" : returnData if list(returnData.keys()) != list() else None
    }

    return returnData

if __name__ == '__main__':
    import pandas as pd

    prompt = input('>> ')
    print(lemmatize(prompt))

    while True:
        prompt = input('Enter a prompt > ')
        if prompt in ['quit', 'exit', 'end', 'bye']:
            break

        response = diagnose(prompt)
        print(response)