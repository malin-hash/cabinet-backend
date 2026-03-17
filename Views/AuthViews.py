from flask import Blueprint, request, jsonify
from Controllers import AvocatController
from flask_jwt_extended import get_jwt_identity, jwt_required
from Models import Avocat


auth_bp = Blueprint("auth_bp", __name__, url_prefix="/user")
@auth_bp.route("/add", methods=['POST'])
def avocat_add():
    data = request.get_json()
    result = AvocatController.avocat_add(data)
    return jsonify(result), result.get("status", 200)

@auth_bp.route('/connect', methods=['POST'])
def avocat_connect():
   return AvocatController.avocat_connect()
    
@auth_bp.route('/me', methods=['GET']) 
@jwt_required()
def avocat_get_me():
    user_id = get_jwt_identity()
    # print("USER ID FROM TOKEN:", user_id)
    avocat = Avocat.query.get(user_id)
    if not avocat:
          return jsonify({"message": "Aucun user trouvé"}), 401
    return (
        avocat.to_dict()
    ), 200

@auth_bp.route('/', methods=['GET']) 
def avocat_get_all():
    return AvocatController.get_all_users()
    
@auth_bp.route('/update/profile/<int:id>', methods=['PUT']) 
def avocat_update_profile(id):
    data = request.get_json()
    result = AvocatController.update_avocat_profile(data, id)
    return jsonify(result), result.get("status", 200)
    
@auth_bp.route('/update/password/<int:id>', methods=['PUT']) 
def avocat_update_password(id):
    data = request.get_json()
    result = AvocatController.update_password(data, id)
    return jsonify(result), result.get("status", 200)
    
@auth_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def client_delete(id):
    user_id = get_jwt_identity()
    return AvocatController.avocat_delete(id, user_id)