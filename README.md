# Hackathon-AgroInsight - SIC 2025
Application mobile pour les agriculteurs avec la puissance de leurs connaissances et leur efficacité dans la plantation et la culture. Cette application est utilisée par l'IA pour résoudre les problèmes et orienter les agriculteurs.


## Option 3 : Désactiver l'alias Windows (temporaire)
Si vous voulez juste désactiver le raccourci Microsoft Store :

Settings > Apps > App execution aliases
Désactivez les alias pour "python.exe" et "python3.exe"

Après installation, vérifiez :
```bash
python --version
# ou
python3 --version

pip --version
```
Pour votre projet Flask/Django :
Une fois Python installé :
bash# Installer les dépendances (si vous avez un requirements.txt)
```
pip install -r requirements.txt
```
# Ou installer Flask manuellement
```
pip install flask
```
# Puis lancer votre app
```
python app.py
```
Si vous utilisez un environnement virtuel :
bash# Créer un environnement virtuel
```
python -m venv venv
```
# L'activer (Windows)
```
Command Prompt:
bash
source venv/bin/activate

cmd

venv\Scripts\activate
PowerShell:

powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

pip install flask
pip install 
pip install flask-cors
pip install openai

