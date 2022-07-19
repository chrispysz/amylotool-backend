from flask import Flask
from firebase_admin import credentials, initialize_app

cred = credentials.Certificate("api/key.json")
default_app = initialize_app(cred)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '0934asbfgds43dfshf5432'
    app.config['TIMEOUT'] = None

    from .sequenceAPI import sequenceAPI

    app.register_blueprint(sequenceAPI, url_prefix='/sequence')

    return app