import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore
from .single_predict import predict_single

db = firestore.client()
subsequence_ref = db.collection('subsequences')

subsequencesAPI = Blueprint('subsequencesAPI', __name__)

@subsequencesAPI.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        id = request.json['id']
        subsequence_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@subsequencesAPI.route('/list', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON.
        todo : Return document that matches query ID.
        all_todos : Return all documents.
    """
    try:
        # Check if ID was passed to URL query
        subsequence_id = request.args.get('id')
        if subsequence_id:
            subsequence = subsequence_ref.document(subsequence_id).get()
            return jsonify(subsequence.to_dict()), 200
        else:
            all_subsequences = [doc.to_dict() for doc in subsequence_ref.stream()]
            return jsonify(all_subsequences), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@subsequencesAPI.route('/update', methods=['POST', 'PUT'])
def update():
    """
        update() : Update document in Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        subsequence_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@subsequencesAPI.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection.
    """
    try:
        # Check for ID in URL query
        subsequence_id = request.args.get('id')
        subsequence_ref.document(subsequence_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@subsequencesAPI.route('/predict', methods=['POST'])
def predict():

    try:
        subsequence = request.json['subsequence']
        result = predict_single(subsequence)
        return jsonify(
                classification=str(result[0]),
                result = str(result[1])
            )
    except Exception as e:
        return f"An Error Occurred: {e}"

