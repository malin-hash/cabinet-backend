from Extensions import db
from Models import Client 
from datetime import datetime, date, time, timedelta
from flask import Blueprint, request, jsonify 
from sqlalchemy import or_, func
from Validator import (
    validate_text,
    validate_number,
    validate_email,
)



class ClientController:
    
    @staticmethod
    def client_add(data):
        if data['name'] and data['firstname'] and data['email'] and data['phoneNumber'] and data['genre'] and data['address'] and data['nationality']  and data['profession']:
            
            if not validate_text(data['name']):
                return {"message": "Le nom doit commencer obligatoirement par une lettre et contenir 2 caractères minimum", "status": 400}
            if not validate_text(data['firstname']):
                return {"message": "Le prénom doit commencer obligatoirement par une lettre et contenir 2 caractères minimum", "status": 400}
            if not validate_email(data['email']):
                return {"message": "Veuillez entrer un email valide", "status": 400}
            if not validate_number(data['phoneNumber']):
                return {"message": "Le numéro doit contenir minimum 8 caractère", "status": 400}
            # if not validate_text(data['profession']):
            #     return {"message": "La profession doit commencer obligatoirement par une lettre et contenir 2 caractères minimum", "status": 400}
            newClient = Client(
                name = data['name'],
                firstname = data['firstname'],
                email = data['email'],
                phoneNumber = data['phoneNumber'],
                genre = data['genre'],
                address = data['address'],
                nationality = data['nationality'],
                profession = data['profession'],
                updated_at=db.func.current_timestamp()

            )
            db.session.add(newClient)
            db.session.commit()
            return {'message': 'Ce Client est ajouté avec succès', 'status':201}
        else:
            return {'message': 'Veuillez remplir tous les champs !', 'status': 401}
            
    @staticmethod
    def client_get_all():
        query_text = request.args.get("q", "").strip()
        if not query_text:
            clients = Client.query.limit(10).all()
        else:
            clients = Client.query.filter(
                or_(
                    Client.name.ilike(f"%{query_text}%"),
                    Client.firstname.ilike(f"%{query_text}%"),
                )
            ).all()
            
        data = [c.to_dict() for c in clients]
        return data
    @staticmethod
    def client_delete(id):
        try:
            client_is_exist = Client.query.filter_by(id=id).first()
        except:
            return {'message': 'Aucun client trouvé', 'status': 401}
            
        db.session.delete(client_is_exist)
        db.session.commit()
        return {'message': 'Ce client est bien supprimé', 'status':201}
        
    @staticmethod
    def client_show(id):
        try:
            client = Client.query.filter_by(id=id).first()
        except:
            return {'message': 'Aucun Client trouvé', 'status': 401}
            
        return {
            'name': client.name,
            'firstname': client.firstname,
            'email': client.email,
            'phoneNumber': client.phoneNumber,
            'genre': client.genre,
            'address': client.address,
            'nationality': client.nationality,
            'profession': client.profession,
        }
        
    @staticmethod
    def client_update(id, data):
        if data['name'] and data['firstname'] and data['email'] and data['phoneNumber'] and data['genre'] and data['address'] and data['nationality']  and data['profession']:
            try:
                client_is_exist = Client.query.filter_by(id=id).first()
            except:
                return {'message': 'Aucun client trouvé', 'status': 401}
            
            if not validate_text(data['name']):
                return {"message": "Le nom doit commencer obligatoirement par une lettre et contenir 2 caractères minimum", "status": 400}
            if not validate_text(data['firstname']):
                return {"message": "Le prénom doit commencer obligatoirement par une lettre et contenir 2 caractères minimum", "status": 400}
            if not validate_email(data['email']):
                return {"message": "Veuillez entrer un email valide", "status": 400}
            if not validate_number(data['phoneNumber']):
                return {"message": "Le numéro doit contenir minimum 8 caractère", "status": 400}
            if not validate_text(data['profession']):
                return {"message": "La profession doit commencer obligatoirement par une lettre et contenir 2 caractères minimum", "status": 400}
            
            client_is_exist.name=data['name'],
            client_is_exist.firstname=data['firstname'],
            client_is_exist.email=data['email'],
            client_is_exist.phoneNumber=data['phoneNumber'],
            client_is_exist.genre=data['genre'],
            client_is_exist.address=data['address'],
            client_is_exist.nationality=data['nationality'],
            client_is_exist.profession=data['profession'],
            
            db.session.commit()
            return {'message': 'Ce Client est modifié avec succès', 'status':201}
        else:
            return {'message': 'Veuillez remplir tous les champs !', 'status': 401}
            
    @staticmethod
    def get_number_client():
        try:
            clients = Client.query.count()
        except:
            return {"message": 'Aucune donnnée trouvée', "status": 401}
        return {
            "clients": clients
        }
        
    @staticmethod
    def clients_per_month():
        data = db.session.query(
            func.strftime("%Y-%m", Client.updated_at),
            func.count(Client.id)
        ).group_by(func.strftime("%Y-%m", Client.updated_at)).all()
        
        result = [{"month": month, "count": count} for month, count in data]
        return result