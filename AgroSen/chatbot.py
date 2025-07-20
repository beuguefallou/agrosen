import tkinter as tk
from tkinter import *
import nltk
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import tflearn
import numpy as np
import random
import pickle
import json
import os
import spacy
import re


nlp = spacy.load('es_core_news_sm')


with open('intents.json', encoding='utf-8') as file:
    data = json.load(file)

def lemmatize_sentence(sentence):
    sentence = sentence.lower()
    sentence = re.sub('[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]', ' ', sentence)
    doc = nlp(sentence)
    lemmas = [token.lemma_ for token in doc]
    print(f"Lemmatized '{sentence}' to {lemmas}")  # Mensaje de depuración
    return lemmas


if os.path.exists("data.pickle"):
    os.remove("data.pickle")
if os.path.exists("model.tflearn.index"):
    os.remove("model.tflearn.index")
if os.path.exists("model.tflearn.meta"):
    os.remove("model.tflearn.meta")
if os.path.exists("model.tflearn.data-00000-of-00001"):
    os.remove("model.tflearn.data-00000-of-00001")

print("Archivos antiguos eliminados, procesando datos y entrenando el modelo desde cero")

words = []
labels = []
docs_x = []
docs_y = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        wrds = nltk.word_tokenize(pattern)
        docs_x.append(wrds)
        docs_y.append(intent['tag'])

        
        words.extend(lemmatize_sentence(pattern))

    if intent['tag'] not in labels:
        labels.append(intent['tag'])

words = sorted(list(set(words)))
labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []
    wrds = lemmatize_sentence(' '.join(doc))

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

training = np.array(training)
output = np.array(output)

with open("data.pickle", "wb") as f:
    pickle.dump((words, labels, training, output), f)

tf.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation='softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net)

model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("model.tflearn")



def bag_of_words(s, words):
    s = s.lower()
    s = re.sub('[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]', ' ', s)  # Se reemplaza por espacio cualquier caracter que no sea letras en español
    bag = [0 for _ in range(len(words))]
    s_words = lemmatize_sentence(s)

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    print(f"Bag of words for '{s}': {bag}")  # Mensaje de depuración
    return np.array(bag)

def chatbot_response(msg):
    bow = bag_of_words(msg, words)
    results = model.predict([bow])
    print(f"Model prediction for '{msg}': {results}")  # Mensaje de depuración
    results_index = np.argmax(results)
    tag = labels[results_index]

    for tg in data['intents']:
        if tg['tag'] == tag:
            responses = tg['responses']
            return random.choice(responses)

    return "Lo siento, no entiendo lo que quieres decir."


base = Tk()  
base.title("Chatbot")  
base.geometry("400x500")  


ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font=("Arial", 12), wrap=WORD)
ChatLog.config(foreground="black")
ChatLog.insert(END, "SALUDOS BIENVENIDO\n\n") 
ChatLog.place(x=6, y=6, height=386, width=370) 


scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set
scrollbar.place(x=376, y=6, height=386)


ChatLog.config(state=DISABLED)


EntryBox = Text(base, bd=0, bg="white", width="29", height="5", font=("Arial", 12), wrap=WORD)
EntryBox.place(x=6, y=401, height=90, width=265)

# Función para enviar un mensaje (se llama cuando se presiona Enter o se hace clic en el botón 'Send')
def send(event=None):
    msg = EntryBox.get("1.0", 'end-1c').strip()  # Obtener el mensaje escrito por el usuario
    EntryBox.delete("0.0", END)  # Limpiar el cuadro de entrada después de enviar el mensaje

    if msg != '':
        ChatLog.config(state=NORMAL)  # Permitir la escritura en el área de texto
        ChatLog.insert(END, "You: " + msg + '\n\n')  # Mostrar el mensaje del usuario en el chat
        ChatLog.config(foreground="black")

        # Obtener la respuesta del chatbot
        res = chatbot_response(msg)
        ChatLog.insert(END, "ChatBOT: " + res + '\n\n')  # Mostrar la respuesta del chatbot en el chat
        ChatLog.config(state=DISABLED)  # Bloquear el área de texto nuevamente
        ChatLog.yview(END)  # Desplazar hacia abajo para mostrar la respuesta más reciente

# Botón para enviar mensajes
SendButton = Button(base, font=("Verdana", 12, 'bold'), text="Send", width="9",
                   height=5, bd=0, bg="blue", activebackground="gold",
                   fg='#ffffff', command=send)
SendButton.place(x=282, y=401, height=90)

# Vincular la tecla Enter para enviar mensajes
base.bind('<Return>', send)

# Iniciar el bucle principal de la interfaz gráfica
base.mainloop()
