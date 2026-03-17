from flask import Flask
import Config
from Extensions import db, jwt
from flask_cors import CORS
import os
# from flask_jwt_extended import JWTManager

from Views.AffaireViews import aff_bp
from Views.RdvViews import rdv_bp
from Views.ClientViews import client_bp
from Views.AuthViews import auth_bp
from Views.FolderViews import folder_bp
from Views.DocumentViews import doc_bp
from Views.FactureViews import facture_bp
from Views.NoteView import note_bp
from Config import UPLOAD_FOLDER

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Création du dossier uploads s'il n'existe pas
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(aff_bp)
    app.register_blueprint(rdv_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(folder_bp)
    app.register_blueprint(doc_bp)
    app.register_blueprint(facture_bp)
    app.register_blueprint(note_bp)

    from Models import Affaire, Rdv, Avocat, Client, Folder, Document, Facture, Note
    
    return app
        
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
    
    