from flask import Flask
from firebase_admin import credentials, initialize_app
from flask_cors import CORS

cred = credentials.Certificate("api/key.json")
default_app = initialize_app(cred)

def create_app():
    application = Flask(__name__)
    CORS(application)
    application.config['SECRET_KEY'] = '0934asbfgds43dfshf5432'
    application.config['TIMEOUT'] = None
    

    from .workspacesAPI import workspacesAPI
    from .predictionsAPI import predictionsAPI

    application.register_blueprint(workspacesAPI, url_prefix='/workspace')
    application.register_blueprint(predictionsAPI, url_prefix='/predict')

    @application.route('/')
    def index():
        return 'amylotool-backend'
    

    return application