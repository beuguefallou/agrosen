@echo off
echo ==============================
echo Création de l'environnement virtuel...
echo ==============================
python -m venv venv

echo ==============================
echo Activation de l'environnement virtuel...
echo ==============================
call venv\Scripts\activate

echo ==============================
echo Installation des dépendances...
echo ==============================
pip install --upgrade pip
pip install nltk
pip install tensorflow==1.15.0
pip install tflearn
pip install numpy
pip install pickle5
pip install spacy

echo ==============================
echo Téléchargement du modèle spaCy (espagnol)...
echo ==============================
python -m spacy download es_core_news_sm

echo ==============================
echo Configuration terminée !
echo ==============================
pause
