from Extensions import db
from Models import Facture, Folder, Client, Avocat
from flask import jsonify, request
from datetime import datetime, date, time, timedelta
import locale
from sqlalchemy import or_

class FactureController:
    
    @staticmethod
    def add_facture(data):
        if  data["folder_id"] and data['nom'] and data["FraisOuverture"]:
            new_facture = Facture(
                folder_id = data["folder_id"],
                nom = data["nom"],
                FraisOuverture = data["FraisOuverture"],
                FraisFirstInstance = data["FraisFirstInstance"],
                FraisAppel = data["FraisAppel"],
                FraisCassation = data["FraisCassation"],
                FraisIncident = data["FraisIncident"],
                FraisFinProcedure = data["FraisFinProcedure"],
            )
            db.session.add(new_facture)
            db.session.commit()
            return {"message": "La factire est bien activée", "status":201}
        else:
            return {"message": "Veuillez remplir tous les champs", "status":401}
            
    
    @staticmethod
    def facture_get_all():
        locale.setlocale(locale.LC_TIME, "fr_FR")
        query_text = request.args.get("q", "").strip()
        if not query_text:
             factures = db.session.query(Facture).join(Folder).join(Client).join(Avocat).order_by(Facture.id.desc()).limit(8)
        else:
             factures = db.session.query(Facture).join(Folder).join(Client).join(Avocat).filter(
                or_(
                    Folder.numero_dossier.ilike(f"%{query_text}%"),
                    Client.name.ilike(f"%{query_text}%"),
                ),
            ).all()
        
        data = [
            {
                'id': t.id,
                'nom': t.nom,
                'FraisOuverture': t.FraisOuverture,
                'FraisFirstInstance': t.FraisFirstInstance,
                'FraisAppel': t.FraisAppel,
                'FraisCassation': t.FraisCassation,
                'FraisIncident': t.FraisIncident,
                'FraisFinProcedure': t.FraisFinProcedure,
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
            } for t in factures
        ]
        return data
        
    
    @staticmethod
    def update_facture(facture_id, data):
        if  data["folder_id"] and data['nom'] and data["FraisOuverture"]:
        
         facture = Facture.query.get(facture_id)
         if not facture:
             return {"message": "Facture non trouvée", "status": 404}
         
         facture.nom = data["nom"]
         facture.FraisOuverture = data["FraisOuverture"]
         facture.FraisFirstInstance = data["FraisFirstInstance"]
         facture.FraisAppel = data["FraisAppel"]
         facture.FraisCassation = data["FraisCassation"]
         facture.FraisIncident = data["FraisIncident"]
         facture.FraisFinProcedure = data["FraisFinProcedure"]
         facture.folder_id = data["folder_id"]
         
         db.session.commit()
         return {"message": "Facture mis à jour avec succès", "status": 200}
         
    @staticmethod
    def delete_facture(facture_id):
        facture = Facture.query.get(facture_id)
        if not facture:
            return {"message": "Facture non trouvée", "status": 404}
        
        db.session.delete(facture)
        db.session.commit()
        return {"message": "Dossier supprimé avec succès", "status": 201}