from flask import Blueprint, request, jsonify 
from Controllers import RdvController

rdv_bp = Blueprint("rdv_bp", __name__)
@rdv_bp.route("/rdv/add", methods=["POST"])
def rdv_add():
    data = request.get_json()
    result = RdvController.advAdd(data)
    return jsonify(result), result.get("status", 200)

@rdv_bp.route("/", methods=["GET"])
def rdv_get_all():
    return RdvController.get_rdv_all()

@rdv_bp.route("/number", methods=["GET"])
def rdv_number():
    return RdvController.get_number_rdv()
    
@rdv_bp.route("/rdv/<int:id>", methods=["DELETE"])
def rdv_delete(id):
    return RdvController.delete_rdv(id)
    
@rdv_bp.route("/rdv/<int:id>", methods=["PUT"])
def rdv_update(id):
    return RdvController.update_rdv(id)