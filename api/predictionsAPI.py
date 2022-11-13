import requests
from flask import Blueprint, request, jsonify


predictionsAPI = Blueprint('predictionsAPI', __name__)


@predictionsAPI.route('/model', methods=['POST'])
def model():
    available_models = [{"model":"AmBERT", "url":"https://amylotool-ambert.onrender.com/predict/full"}]

    try:
        model = request.json['model']
        sequence = request.json['sequence']
        for m in available_models:
            if m['model'] == model:
                response = requests.post(m['url'], json={"sequence":sequence})
                return response.json()
            else:
                return jsonify({"error":"Model not found"}), 404
    except Exception as e:
        return f"An Error Occurred: {e}"

