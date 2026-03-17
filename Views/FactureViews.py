from flask import Blueprint, request, jsonify 
from Controllers import FactureController

facture_bp = Blueprint("facture_bp", __name__)

@facture_bp.route("/facture", methods=['POST'])
def factures_add():
    data = request.get_json()
    result = FactureController.add_facture(data)
    return jsonify(result), result.get("status", 200)
    
@facture_bp.route('/facture', methods=['GET'])
def get_all_factures():
   return jsonify(FactureController.facture_get_all())
   
@facture_bp.route('/facture/<int:facture_id>', methods=['PUT'])
def update_facture(facture_id):
    data = request.get_json()
    result = FactureController.update_facture(facture_id, data)
    return jsonify(result), result['status']
    
@facture_bp.route('/facture/<int:facture_id>', methods=['DELETE'])
def delete_facture(facture_id):
    return FactureController.delete_facture(facture_id)