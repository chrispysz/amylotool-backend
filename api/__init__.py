from flask import Flask
from firebase_admin import credentials, initialize_app
from flask_cors import CORS

cred = credentials.Certificate("api/key.json")
default_app = initialize_app(cred)

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = '0934asbfgds43dfshf5432'
    app.config['TIMEOUT'] = None
    

    from .workspacesAPI import workspacesAPI
    from .sequencesAPI import sequencesAPI

    app.register_blueprint(workspacesAPI, url_prefix='/workspace')
    app.register_blueprint(sequencesAPI, url_prefix='/sequence')

    return app