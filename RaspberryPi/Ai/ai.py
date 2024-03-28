from training import training
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
def lem(sentence):
    words = []
    for word in sentence.split(' '):
        lem_order_of_importance = [
            lemmatizer.lemmatize(word, 'n'),
            lemmatizer.lemmatize(word, 'v'),
            lemmatizer.lemmatize(word, 'r'),
            lemmatizer.lemmatize(word, 'a')
        ]
        for lemmed in lem_order_of_importance:
            if lemmed != word:
                words.append(lemmed)
                break
        else:
            words.append(lemmed)
    return ' '.join(words)

def diagnose(prompt):
    returnData = {}
    likeliest_val = 0
    likeliest_name = ''
    for diagnosis in training: # loop over all trained illnesses
        likelyhood = 0 # chance disease is a match
        symptoms = training[diagnosis]['symptoms']
        for symptom in symptoms:
            if lem(symptom) in lem(prompt):
                # symptom is a "match"
                likelyhood += 1
        
        # make rarer disease show up as less likely
                
        likelyhood *= 10 - training[diagnosis]['rarity']

        if likelyhood != 0:
            returnData[diagnosis] = training[diagnosis]
            returnData[diagnosis]['chance'] = likelyhood

        if likelyhood > likeliest_val:
            # mark as the likeliest
            likeliest_name = diagnosis
            likeliest_val = likelyhood

    if likeliest_name == '':
        returnData = {
            "diagnosis" : None,
            "other" : None,
        }
    else:
        returnData.pop(likeliest_name)
        returnData = {
            "diagnosis" : {likeliest_name: training[likeliest_name]},
            "other" : returnData
        }

    return returnData

def fill(diagnosis, symptoms):
    pass

if __name__ == '__main__':
    prompt = ''
    while prompt not in ['end', 'quit', 'halt', 'done', 'bye']:
        prompt = input('Enter a prompt > ')
        print(diagnose(prompt))