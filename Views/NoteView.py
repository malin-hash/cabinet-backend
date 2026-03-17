from flask import Blueprint, request, jsonify 
from Controllers import NoteController

note_bp = Blueprint("note_bp", __name__)

@note_bp.route("/note", methods=['POST'])
def notes_add():
    data = request.get_json()
    result = NoteController.createNote(data)
    return jsonify(result), result.get("status", 200)
    
@note_bp.route('/note', methods=['GET'])
def get_all_notes():
   return jsonify(NoteController.getAllNotes())
   
@note_bp.route('/note/<int:note_id>', methods=['PUT'])
def update_notes(note_id):
    data = request.get_json()
    result = NoteController.update_note(note_id, data)
    return jsonify(result), result['status']
    
@note_bp.route('/note/<int:note_id>', methods=['DELETE'])
def delete_facture(note_id):
    return NoteController.delete_note(note_id)