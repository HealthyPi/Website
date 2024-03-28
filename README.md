# Healthy Pi Website
## back-end
The backend is written in Python using flask, just a disclaimer it is not a RESTful API.
It has a GET and POST request, GET for the website front-end [healthbotai.pythonanywhere.com](https://healthbotai.pythonanywhere.com/) and POST for querying the ai.
### POST requests
it's at https://healthbotai.pythonanywhere.com/chatbot
Here's an example of quering the chatbot in JavaScript. It does not support CORS.
```javascript
fetch ('https://healthbotai.pythonanywhere.com/chatbot', {
  method: 'POST',
  headers: {
  'Content-Type': 'application/json'
  },
  body: {
    purpose: 'query',
    prompt: 'this is where your prompt for the ai goes'
  }
})
.then(response => {
  return response.json()
})
.then(json => {
  console.table(json)
})
```
### Response
```json
"diagnosis": {},
"other": {}
```
## front-end
Unfortunately, the front end is not written using Python. It is made using react.

## AI
The AI however, is written in Python. It is not a large language model and all its response are predictable and non-random.
Basically we have all our training in /training.py, which is a large Python dictionary with lots of diagnosis and symptoms. The ai then using nltk word lemmatizer to reduce the prompt and symptoms to their most basic meaning and checks weather are given symptom appears in the prompt. What makes it machine learning is you can train the ai by adding more data. See Ai/ai.py for the specific code.