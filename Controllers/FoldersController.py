from Extensions import db
from Models import Folder, Client, Avocat, Affaire
from Utils import generate_unique_code
from flask import jsonify, request
from sqlalchemy import or_, func
# from datetime import datetime, date, time, timedelta


class FoldersController:
    @staticmethod
    def create_folder(data):
    
        if( not data.get('description') or not data.get('client_id') or not data.get('avocat_id') or not data.get('affaire_id')):
            return {"message": "Veuillez remplir tous les champs", "status": 401} # Required fields are missing
            
        new_folder = Folder(
            description=data.get('description'),
            numero_dossier=generate_unique_code(),
            client_id=data.get('client_id'),
            avocat_id=data.get('avocat_id'),
            affaire_id=data.get('affaire_id'),
            created_at=db.func.current_timestamp(),
            updated_at=db.func.current_timestamp()
        )
        db.session.add(new_folder)
        db.session.commit()
        return {"message": "Dossier créé avec succès", "status": 201}

    @staticmethod
    def get_all_folders():
        query_text = request.args.get("q", "").strip()
        if not query_text:
            folders = db.session.query(Folder).join(Client).join(Avocat).join(Affaire).filter(Folder.is_archive==False).order_by(Client.name.asc()).limit(6)
        else:
            folders = db.session.query(Folder).join(Client).join(Avocat).join(Affaire).filter(
                or_(
                    Client.name.ilike(f"%{query_text}%"),
                    Folder.numero_dossier.ilike(f"%{query_text}%"),
                ),
                Folder.is_archive==False,
            ).all()

        folder_data =[
        {
            "id": t.id,
            "description": t.description,
            "numero_dossier": t.numero_dossier,
            "client": {
                "id": t.client.id,
                "name": t.client.name,
                "email": t.client.email
            },
            "avocat": {
                "id": t.avocat.id,
                "name": t.avocat.name,
                "email": t.avocat.email
            },
            "affaire": {
                "id": t.affaire.id,
                "title": t.affaire.title,
            },
            "created_at": t.created_at.strftime("%d %B %Y"),
            "updated_at": t.updated_at
        }for t in folders
        ]
        return folder_data
        
    
    @staticmethod
    def get_folder_by_id(folder_id):
        folder = db.session.query(Folder).join(Client).join(Avocat).join(Affaire).filter_by(Folder.id==folder_id).first()
        if not folder:
            return {"message": "Dossier non trouvé", "status": 404}
        
        return {
             "id": folder.id,
            "description": folder.description,
            "numero_dossier": folder.numero_dossier,
            "client": {
                "id": folder.client.id,
                "name": folder.client.name,
                "email": folder.client.email
            },
            "avocat": {
                "id": folder.avocat.id,
                "name": folder.avocat.name,
                "email": folder.avocat.email
            },
            "affaire": {
                "id": folder.affaire.id,
                "title": folder.affaire.title,
            },
            "created_at": folder.created_at.strftime("%d %B %Y"),
            "updated_at": folder.updated_at
        }, 200
    @staticmethod
    def delete_folder(folder_id):
        folder = Folder.query.get(folder_id)
        if not folder:
            return {"message": "Dossier non trouvé", "status": 404}
        
        db.session.delete(folder)
        db.session.commit()
        return {"message": "Dossier supprimé avec succès", "status": 201}
    
    @staticmethod
    def update_folder(folder_id, data):
        if( not data.get('description') or not data.get('client_id') or not data.get('avocat_id') or not data.get('affaire_id')):
            return {"message": "Veuillez remplir tous les champs", "status": 401} # Required fields are missing
        
        folder = Folder.query.get(folder_id)
        if not folder:
            return {"message": "Dossier non trouvé", "status": 404}
        
        folder.description = data["description"]
        folder.client_id = data["client_id"]
        folder.avocat_id = data["avocat_id"]
        folder.affaire_id = data["affaire_id"]
        folder.updated_at = db.func.current_timestamp()
        
        db.session.commit()
        return {"message": "Dossier mis à jour avec succès", "status": 200}
        
    def archive_folder(folder_id):
        
        folder = Folder.query.get(folder_id)
        if not folder:
            return {"message": "Dossier non trouvé", "status": 404}
        
        folder.is_archive = True
        folder.updated_at = db.func.current_timestamp()
        
        db.session.commit()
        return {"message": "Dossier archivé avec succès", "status": 200}
        
    def no_archive_folder(folder_id):
        
        folder = Folder.query.get(folder_id)
        if not folder:
            return {"message": "Dossier non trouvé", "status": 404}
        
        folder.is_archive = False
        folder.updated_at = db.func.current_timestamp()
        
        db.session.commit()
        return {"message": "Dossier désarchivé avec succès", "status": 200}
        
    @staticmethod
    def get_number_folder():
        try:
            folders = Folder.query.filter_by(is_archive=True).count()
        except:
            return {"message": 'Aucune donnnée trouvée', "status": 401}
        return {
            "folders": folders
        }
        
    @staticmethod
    def get_all_folders_archive():
        query_text = request.args.get("q", "").strip()
        if not query_text:
            folders = db.session.query(Folder).join(Client).join(Avocat).join(Affaire).filter(Folder.is_archive==True).order_by(Client.name.asc()).limit(6)
        else:
            folders = db.session.query(Folder).join(Client).join(Avocat).join(Affaire).filter(
                or_(
                    Client.name.ilike(f"%{query_text}%"),
                    Folder.numero_dossier.ilike(f"%{query_text}%"),
                ),
                Folder.is_archive==True,
            ).all()
        folder_data =[
        {
            "id": t.id,
            "description": t.description,
            "numero_dossier": t.numero_dossier,
            "client": {
                "id": t.client.id,
                "name": t.client.name,
                "email": t.client.email
            },
            "avocat": {
                "id": t.avocat.id,
                "name": t.avocat.name,
                "email": t.avocat.email
            },
            "affaire": {
                "id": t.affaire.id,
                "title": t.affaire.title,
            },
            "created_at": t.created_at.strftime("%d %B %Y"),
            "updated_at": t.updated_at
        }for t in folders
        ]
        return folder_data
    
    @staticmethod
    def get_number_folder_not_archive():
        try:
            noarchive = Folder.query.filter_by(is_archive=False).count()
        except:
            return {"message": 'Aucune donnnée trouvée', "status": 401}
        return {
            "noarchive": noarchive
        }
    
    @staticmethod
    def get_number_folder_archive():
        try:
             archive = Folder.query.filter_by(is_archive=True).count()
        except:
            return {"message": 'Aucune donnnée trouvée', "status": 401}
        return {
            "archive": archive
        }
        
    @staticmethod
    def get_number_folder_per_month():
        try:
            data = db.session.query(
                func.strftime("%Y-%m", Folder.updated_at).label("month"),
                func.count(Folder.id).label("count")
            ).group_by(func.strftime("%Y-%m", Folder.updated_at)).all()
            
            result = [{"month": month, "count": count} for month, count in data]
            return result
        except:
            return {"message": 'Aucune donnnée trouvée', "status": 401}
        