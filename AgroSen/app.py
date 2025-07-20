from flask import Flask, request, render_template, jsonify
import spacy
import json
import re
import tflearn
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np
import random
import pickle

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Cargar modelo de spaCy en español
nlp = spacy.load('es_core_news_sm')

# Cargar los datos de intents desde el archivo JSON
with open('intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

# Cargar los datos de entrenamiento y las etiquetas
with open("data.pickle", "rb") as f:
    words, labels, training, output = pickle.load(f)

# Define la arquitectura del modelo
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation='softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net)

# Cargar el modelo
model.load('model.tflearn')

def lemmatize_sentence(sentence):
    sentence = sentence.lower()
    sentence = re.sub('[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]', ' ', sentence)
    doc = nlp(sentence)
    lemmas = [token.lemma_ for token in doc]
    return lemmas

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-záéíóúñü\s]', '', text)
    return text

def bag_of_words(s, words):
    s = s.lower()
    s = re.sub('[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]', ' ', s)
    bag = [0 for _ in range(len(words))]
    s_words = lemmatize_sentence(s)

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    message = data['message']
    response = chatbot_response(message)
    return jsonify({'response': response})

def chatbot_response(msg):
    msg = clean_text(msg)
    doc = nlp(msg)
    
    for ent in doc.ents:
        if ent.label_ == "LOC":  # Detectar si hay una entidad de tipo ubicación
            return f"Procesando ubicación: {ent.text}"
    
    bow = bag_of_words(msg, words)
    results = model.predict([bow])
    results_index = np.argmax(results)
    tag = labels[results_index]

    for tg in intents['intents']:
        if tg['tag'] == tag:
            responses = tg['responses']
            return random.choice(responses)

    return "No entendí tu mensaje. ¿Puedes especificar más detalles?"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
