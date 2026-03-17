from flask import Blueprint, jsonify 
from Controllers import DocumentController

doc_bp = Blueprint("doc_bp", __name__)
@doc_bp.route("/doc", methods=["POST"])
def doc_add():
    data, status = DocumentController.uploads_files()
    return jsonify(data), status

@doc_bp.route("/doc/<int:id>", methods=["PUT"])
def doc_update(id):
    data, status = DocumentController.update_file(id)
    return jsonify(data), status
@doc_bp.route("/doc", methods=["GET"])
def doc_get_all():
    data = DocumentController.get_all_documents()
    return data
    
@doc_bp.route("/doc/<int:doc_id>/view", methods=["GET"])
def doc_get_one(doc_id):
    data = DocumentController.view_document(doc_id)
    return data
    
@doc_bp.route("/doc/<int:document_id>", methods=["DELETE"])
def doc_delete(document_id):
    return DocumentController.delete_document(document_id)