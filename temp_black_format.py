from Extensions import db
from Models import Folder as FolderModels, Client, Avocat, Affaire
from Utils import generate_unique_code


class FoldersController:
    @staticmethod
    def create_folder(data):
    
        if( not data.get('description') or not data.get('client_id') or not data.get('avocat_id') or not data.get('affaire_id')):
            return {"message": "Veuillez remplir tous les champs", "status": 401} # Required fields are missing
            
        new_folder = FolderModels(
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
        folders = db.session.query(FolderModels, Client, Avocat, Affaire).join(Client, FolderModels.client_id == Client.id).join(
            Avocat, FolderModels.avocat_id == Avocat.id).join(Affaire, FolderModels.affaire_id == Affaire.id).all()
        folder_list = []
        for folder, client, avocat, affaire in folders:
            folder_data = {
                "id": folder.id,
                "description": folder.description,
                "numero_dossier": folder.numero_dossier,
                "client": {
                    "id": client.id,
                    "name": client.name,
                    "email": client.email
                },
                "avocat": {
                    "id": avocat.id,
                    "name": avocat.name,
                    "email": avocat.email
                },
                "affaire": {
                    "id": affaire.id,
                    "title": affaire.title,
                    "status": affaire.status
                },
                "created_at": folder.created_at,
                "updated_at": folder.updated_at
            }
            folder_list.append(folder_data)
        return {"folders": folder_list, "status": 200}
        
    
    @staticmethod
    def get_folder_by_id(folder_id):
        folder = FolderModels.query.get(folder_id)
        if not folder:
            return {"message": "Dossier non trouvé", "status": 404}
        
        folder_data = {
            "id": folder.id,
            "description": folder.description,
            "numero_dossier": folder.numero_dossier,
            "client_id": folder.client_id,
            "avocat_id": folder.avocat_id,
            "affaire_id": folder.affaire_id,
            "created_at": folder.created_at,
            "updated_at": folder.updated_at
        }
        return {"folder": folder_data, "status": 200}
    
    @staticmethod
    def delete_folder(folder_id):
        folder = FolderModels.query.get(folder_id)
        if not folder:
            return {"message": "Dossier non trouvé", "status": 404}
        
        db.session.delete(folder)
        db.session.commit()
        return {"message": "Dossier supprimé avec succès", "status": 200}
    
    @staticmethod
    def update_folder(folder_id, data):
        if not data:
            return {"message": "Aucune donnée fournie pour la mise à jour", "status": 400}
        if not (data.get('description') or data.get('client_id') or data.get('avocat_id') or data.get('affaire_id')):
            return {"message": "Au moins un champ doit être fourni pour la mise à jour", "status": 400}
        
        folder = FolderModels.query.get(folder_id)
        if not folder:
            return {"message": "Dossier non trouvé", "status": 404}
        
        folder.description = data.get('description', folder.description)
        folder.client_id = data.get('client_id', folder.client_id)
        folder.avocat_id = data.get('avocat_id', folder.avocat_id)
        folder.affaire_id = data.get('affaire_id', folder.affaire_id)
        folder.updated_at = db.func.current_timestamp()
        
        db.session.commit()
        return {"message": "Dossier mis à jour avec succès", "status": 200}