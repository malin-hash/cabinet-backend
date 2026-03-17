from flask import Blueprint, request, jsonify 
from Controllers import AffaireController

aff_bp = Blueprint("aff_bp", __name__)
@aff_bp.route("/affaire", methods=["GET"])
def archive_all():
    return AffaireController.get_aff_all()
