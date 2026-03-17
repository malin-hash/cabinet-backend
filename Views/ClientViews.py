from flask import Blueprint, request, jsonify 
from Controllers import ClientController

client_bp = Blueprint("client_bp", __name__)
@client_bp.route("/client/search", methods=["GET"])
def clients_all():
    data = ClientController.client_get_all()
    return jsonify(data)
    
@client_bp.route("/client/number", methods=["GET"])
def clients_number():
    return ClientController.get_number_client()

@client_bp.route("/client/add", methods=['POST'])
def clients_add():
    data = request.get_json()
    result = ClientController.client_add(data)
    return jsonify(result), result.get("status", 200)
    
@client_bp.route('/client/<int:id>', methods=['DELETE'])
def client_delete(id):
    return ClientController.client_delete(id)
    
@client_bp.route('/client/<int:id>', methods=['GET'])
def client_show(id):
    return ClientController.client_show(id)
    
@client_bp.route('/client/<int:id>', methods=['PUT'])
def client_update(id):
    data = request.get_json()
    result = ClientController.client_update(id, data)
    return jsonify(result), result.get("status", 200)
    
@client_bp.route('/client/month', methods=['GET'])
def client_per():
    return ClientController.clients_per_month()
    