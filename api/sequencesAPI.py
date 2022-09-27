import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore
from .single_predict import predict_single

db = firestore.client()
sequence_ref = db.collection('sequences')

sequencesAPI = Blueprint('sequencesAPI', __name__)

@wsequencesAPI.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        id = request.json['id']
        sequence_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@sequencesAPI.route('/list', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON.
        todo : Return document that matches query ID.
        all_todos : Return all documents.
    """
    try:
        # Check if ID was passed to URL query
        sequence_id = request.args.get('id')
        if sequence_id:
            sequence = sequence_ref.document(sequence_id).get()
            return jsonify(sequence.to_dict()), 200
        else:
            all_sequences = [doc.to_dict() for doc in sequence_ref.stream()]
            return jsonify(all_sequences), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@sequencesAPI.route('/update', methods=['POST', 'PUT'])
def update():
    """
        update() : Update document in Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        sequence_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@sequencesAPI.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection.
    """
    try:
        # Check for ID in URL query
        sequence_id = request.args.get('id')
        sequence_ref.document(sequence_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@sequencesAPI.route('/predict', methods=['POST'])
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

