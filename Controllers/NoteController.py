from Models import Note, Folder, Client, Avocat
from Extensions import db
from flask import jsonify, request
from sqlalchemy import or_



class NoteController:
    @staticmethod
    def createNote(data):
        if  data["folder_id"] and data['description']:
            new_note = Note(
                folder_id = data["folder_id"],
                description = data["description"],
            )
            db.session.add(new_note)
            db.session.commit()
            return {"message": "La note est bien ajoutée", "status":201}
        else:
            return {"message": "Veuillez remplir tous les champs", "status":401}
    
    @staticmethod
    def getAllNotes():
        query_text = request.args.get("q", "").strip()
        if not query_text:
             notes = db.session.query(Note).join(Folder).join(Client).join(Avocat).order_by(Note.id.desc()).filter(Folder.is_archive == False).limit(8)
        else:
             notes = db.session.query(Note).join(Folder).join(Client).join(Avocat).filter(
                or_(
                    Folder.numero_dossier.ilike(f"%{query_text}%"),
                    Client.name.ilike(f"%{query_text}%"),
                    Avocat.name.ilike(f"%{query_text}%"),
                ),
                Folder.is_archive == False
            ).all()
        data = [
            {
                'id': t.id,
                'description': t.description,
                "folder": {
                    "id": t.folder.id,
                    "numero_dossier": t.folder.numero_dossier,
                    "client": {
                        "id": t.folder.client.id,
                        "name": t.folder.client.name,
                        "firstname": t.folder.client.firstname,
                        "phoneNumber": t.folder.client.phoneNumber,
                        "address": t.folder.client.address,
                        "nationality": t.folder.client.nationality,
                    },
                    "avocat": {
                        "id": t.folder.avocat.id,
                        "name": t.folder.avocat.name,
                        "firstname": t.folder.avocat.firstname,
                        "email": t.folder.avocat.email,
                        "phoneNumber": t.folder.avocat.phoneNumber,
                    }
               },
            } for t in notes
        ]
        return data
        
    @staticmethod
    def update_note(note_id, data):
        if  data["folder_id"] and data['description']:
        
         note = Note.query.get(note_id)
         if not note:
             return {"message": "note non trouvée", "status": 404}
         
         note.description = data["description"]
         note.folder_id = data["folder_id"]
         
         db.session.commit()
         return {"message": "note mise à jour avec succès", "status": 200}
    
    @staticmethod
    def delete_note(note_id):
        note = Note.query.get(note_id)
        if not note:
            return {"message": "note non trouvée", "status": 404}
        
        db.session.delete(note)
        db.session.commit()
        return {"message": "Note supprimée avec succès", "status": 201}