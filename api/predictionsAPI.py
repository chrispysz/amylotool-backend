import requests
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin


predictionsAPI = Blueprint('predictionsAPI', __name__)


@predictionsAPI.route('/model', methods=['POST'])
@cross_origin()
def model():
    available_models = [{"model":"AmBERT", "url":"https://amylotool-ambert.herokuapp.com/predict/full"},
    {"model":"ProteinBERT", "url":"https://amylotool-proteinbert-xt1.azurewebsites.net/predict/full"}]

    try:
        model = request.json['model']
        sequence = request.json['sequence']
        process = False
        for m in available_models:
            if m['model'] == model:
                process = True
        if process:
            response = requests.post(m['url'], json={"sequence":sequence})
            return response.json()
        else:
            return jsonify({"error":"Model not found"}), 404
    except Exception as e:
        return f"An Error Occurred: {e}"

