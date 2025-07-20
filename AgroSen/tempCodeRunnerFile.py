from flask import Flask, request, render_template, jsonify
import spacy
import json
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')

# Cargar modelo de spaCy en español
nlp = spacy.load('es_core_news_sm')

# Cargar los datos de intents desde el archivo JSON
with open('intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-záéíóúñü\s]', '', text)
    return text

@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        data = request.get_json(force=True)
        print(f"Datos recibidos: {data}")  # Para depuración
        message = data['message']
        response = chatbot_response(message)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'response': 'Error procesando la solicitud.'}), 400

def chatbot_response(msg):
    msg = clean_text(msg)
    print(f"Mensaje limpio: {msg}")  # Para depuración
    doc = nlp(msg)
    
    for ent in doc.ents:
        if ent.label_ == "LOC":  # Detectar si hay una entidad de tipo ubicación
            return f"Procesando ubicación: {ent.text}"
    
    # Si no se encuentra una ubicación, buscar en los intents
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if clean_text(pattern) in msg:
                return intent['responses'][0]  # Devolver la primera respuesta

    return "No entendí tu mensaje. ¿Puedes especificar más detalles?"

if __name__ == '__main__':
    app.run(debug=True)
