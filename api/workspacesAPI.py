import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore
from .single_predict import predict_single

db = firestore.client()
workspace_ref = db.collection('workspaces')

workspacesAPI = Blueprint('workspacesAPI', __name__)

@workspacesAPI.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        id = request.json['id']
        workspace_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@workspacesAPI.route('/list', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON.
        todo : Return document that matches query ID.
        all_todos : Return all documents.
    """
    try:
        # Check if ID was passed to URL query
        workspace_id = request.args.get('id')
        if workspace_id:
            workspace = workspace_ref.document(workspace_id).get()
            return jsonify(workspace.to_dict()), 200
        else:
            all_workspaces = [doc.to_dict() for doc in workspace_ref.stream()]
            return jsonify(all_workspaces), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@workspacesAPI.route('/update', methods=['POST', 'PUT'])
def update():
    """
        update() : Update document in Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        workspace_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@workspacesAPI.route('/delete', methods=['GET', 'DELETE'])
def delete():
    """
        delete() : Delete a document from Firestore collection.
    """
    try:
        # Check for ID in URL query
        workspace_id = request.args.get('id')
        workspace_ref.document(workspace_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

@workspacesAPI.route('/predict', methods=['POST'])
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

