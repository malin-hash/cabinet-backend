from Extensions import db
from Models import Avocat
from flask_jwt_extended import create_access_token
from flask import jsonify, request
from sqlalchemy import or_
from Validator import (
    validate_text,
    validate_number,
    validate_birth_date,
    validate_email,
    validate_address,
    validate_password
)
class AvocatController:
    
    @staticmethod
    def avocat_add(data):
        if data['name'] and data['firstname'] and data['email'] and data['phoneNumber'] and data['genre'] and data['address'] and data['nationality'] and data['function'] and data['is_admin']:
            
            if not validate_text(data['name']):
                return {"message": "Le nom doit commencer obligatoirement par une lettre et contenir 2 caractères minimum", "status": 400}
            if not validate_text(data['firstname']):
                return {"message": "Le Prénom doit commencer obligatoirement par une lettre et contenir 2 caractères minimum", "status": 400}
            if not validate_email(data['email']):
                return {"message": "Cette adresse E-mail est invalide", "status": 400}
            if not validate_number(data['phoneNumber']):
                return {"message": "Le numéro doit faire 8 chiffres", "status": 400}
            if not validate_address(data['address']):
                return {"message": "L'adresse doit contenir 2 caractères minimum", "status": 400}
            if not validate_text(data['function']):
                return {"message": "La fonction doit commencer obligatoirement par une lettre et contenir 2 caractères minimum", "status": 400}
            users = Avocat.query.filter_by(email=data['email']).first()
            if users:
                return {'message': 'Cet avocat existe déja', 'status': 401}
            
            mdp = "1234"
            new_avocat = Avocat(
                name = data['name'],
                firstname = data['firstname'],
                email = data['email'],
                phoneNumber = data['phoneNumber'],
                genre = data['genre'],
                address = data['address'],
                nationality = data['nationality'],
                function = data['function'],
            )
            new_avocat.set_password(mdp)
            new_avocat.is_admin=int(data['is_admin'])
            db.session.add(new_avocat)
            db.session.commit()
            return {'message':'Le maitre est bien ajouté', 'status':201}
            
        else:
            return {'message': 'Veuillez remplir tous les champs !!!', 'status': 401}
            
    @staticmethod
    def avocat_connect():
        data = request.get_json()
        if data['email'] and data['password']:
          
          avocat = Avocat.query.filter_by(email=data['email']).first()
          if not avocat:
              return jsonify({"message": "L'adresse e-mail ou le mot de passe incorrect"}), 401
          if not avocat.check_password(data["password"]):
              return jsonify({"message": "L'adresse e-mail ou le mot de passe incorrect"}), 401
          
          access_token = create_access_token(identity=str(avocat.id))
          
          return jsonify({"access_token": access_token}), 200
          
        else:
            return jsonify({"message": "Veuillez remplir tous les champs"}), 401
        
    @staticmethod
    def get_all_users():
        query_text = request.args.get("q", "").strip()
        if not query_text:
            avocats = Avocat.query.all()
        else:
            avocats = Avocat.query.filter(
                or_(
                    Avocat.name.ilike(f"%{query_text}%"),
                    Avocat.firstname.ilike(f"%{query_text}%"),
                )
            ).all()
            
        data = [c.to_dict() for c in avocats]
        return data
    
    @staticmethod
    def update_avocat_profile(data, user_id):
        if data['name'] and data['firstname'] and data['email'] and data['phoneNumber'] and data['genre'] and data['address'] and data['nationality'] and data['function']:
            
            if not validate_text(data['name']):
                return {"message": "Le nom doit commencer obligatoirement par une lettre et contenir 2 caractères minimum", "status": 400}
            if not validate_text(data['firstname']):
                return {"message": "Le Prénom doit commencer obligatoirement par une lettre et contenir 2 caractères minimum", "status": 400}
            if not validate_email(data['email']):
                return {"message": "Cette adresse E-mail est invalide", "status": 400}
            if not validate_number(data['phoneNumber']):
                return {"message": "Le numéro doit faire 8 chiffres", "status": 400}
            if not validate_address(data['address']):
                return {"message": "L'adresse doit contenir 2 caractères minimum", "status": 400}
            if not validate_text(data['function']):
                return {"message": "La fonction doit commencer obligatoirement par une lettre et contenir 2 caractères minimum", "status": 400}
            
            avocat = Avocat.query.get(user_id)
            if not avocat:
               return jsonify({"message": "Aucun user trouvé"}), 401
            avocat.name = data['name'],
            avocat.firstname = data['firstname'],
            avocat.email = data['email'],
            avocat.phoneNumber = data['phoneNumber'],
            avocat.genre = data['genre'],
            avocat.address = data['address'],
            avocat.nationality = data['nationality'],
            avocat.function = data['function']
            
            db.session.commit()
            return {'message': 'Votre profile est modifié avec succès', 'status':201}
            
        else:
            return {'message': 'Veuillez remplir tous les champs !!!', 'status': 401}
    @staticmethod
    def update_password(data, user_id):
        if data['password'] and data['newpassword'] and data['confirmpassword']:
            message = (
                'Le nouveau mot de passe n\'est pas fort il doit contenir :'
                "- Au moins 12 carractères\n"
                "- Au moins une minuscule\n"
                "- Au moins un chiffre\n"
                "- Au moins un caractère spécial\n"
            )
        
            avocat = Avocat.query.get(user_id)
            if not avocat:
               return {"message": "Aucun user trouvé"}, 401
            if not avocat.check_password(data["password"]):
               return {'message': 'Ancien mot de passe incorrect !!!', 'status': 401}
            if data['newpassword'] != data['confirmpassword']:
               return {'message': 'Les deux nouveaux mots de passes ne sont pas identiques', 'status': 401}
            if data['newpassword'] == data['password']:
               return {'message': 'Aucune modification est faite', 'status': 401}
            if not validate_password(data['newpassword']):
                return {"message": message , "status": 400}
            
            avocat.set_password(data['newpassword']) 
            db.session.commit()
            return {'message': 'Votre mot de passe est modifié avec succès', 'status':201}
                
        else:
            return {'message': 'Veuillez remplir tous les champs !!!', 'status': 401}
            
    @staticmethod
    def avocat_delete(id, user_id):
        try:
            avocat_is_exist = Avocat.query.filter_by(id=id).first()
        except:
            return {'message': 'Aucun avocat trouvé', 'status': 401}
        if int(id) == int(user_id):
            return {'message': 'Vous ne pouvez pas supprimer votre propre compte car vous êtes actuellement connecté sur celui-ci', 'status':401}
            
        db.session.delete(avocat_is_exist)
        db.session.commit()
        return {'message': avocat_is_exist.function + " Supprimé avec succès", 'status':201}