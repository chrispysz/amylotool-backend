import uuid
from flask import Blueprint, request, jsonify
from .single_predict import predict_single


predictionsAPI = Blueprint('predictionsAPI', __name__)

@predictionsAPI.route('/single', methods=['POST'])
def predict():

    try:
        sequence = request.json['sequence']
        result = predict_single(sequence)
        return jsonify(
                classification=str(result[0]),
                result = str(result[1])
            )
    except Exception as e:
        return f"An Error Occurred: {e}"

