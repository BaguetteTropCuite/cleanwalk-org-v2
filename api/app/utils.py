# utils.py
import hashlib
from flask import current_app
from werkzeug.utils import secure_filename
import os
from google.oauth2 import id_token
from google.auth.transport import requests

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

def verify_google_token(token):
    try:
        # Valide le token reçu de Google
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        
        # Si la validation réussit, retourne les informations utilisateur
        return {
            'google_id': idinfo['sub'],
            'email': idinfo['email'],
            'name': idinfo.get('name'),
            'picture': idinfo.get('picture')
        }
    except ValueError:
        # Si le token est invalide, retourne None
        return None

def validate_api_key(api_key):
    # Get the API key from app.config
    app_api_key = current_app.config.get('API_KEY')
    print(app_api_key)

    # Compare the api_key from the header with the one from app.config
    return api_key == app_api_key

def hash_password(password, salt):
    salted_password = salt + password.encode('utf-8')
    hashed_password = hashlib.sha256(salted_password).hexdigest()
    return hashed_password

def upload_img(image):
    # Check if the image is allowed
    if '.' in image.filename and image.filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']:
        filename = secure_filename(image.filename)
        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return filename
    else:
        return None