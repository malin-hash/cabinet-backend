from Extensions import db 
from Models import Document, Folder
from werkzeug.utils import secure_filename
from flask import send_file, request, jsonify
import os
from Utils import allowed_mime, allowed_extension 
from Config import ALLOWED_EXTENSIONS, ALLOWED_MIMES_TYPE, UPLOAD_FOLDER
from sqlalchemy import or_

class DocumentController:
    
    @staticmethod
    def uploads_files():
        # Upload de plusieurs documents liés à un dossier
        dossier_id = request.form.get("folder_id")
        files = request.files.getlist("files")
        
        print("FILES", request.files)
        print("FORM", request.form)
        # Verification dossier
        if not dossier_id:
            return {"message": "Dossier manquant"}, 401
        
        # Vérification fichiers
        if not files:
            return {"message": "Aucun fichier envoyer", "status": 400}
            
        saved = []
        for file in files:
        
            if file.filename == '':
                continue
            if not allowed_extension(file.filename, ALLOWED_EXTENSIONS):
                return {"message": "Extension non autorisée"}, 400
                
            if not allowed_mime(file.mimetype, ALLOWED_MIMES_TYPE):
                return {"message": "Type MIME non autorisé"}, 400
                
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            document = Document(
                filename = filename,
                filepath = filepath,
                mimetype = file.mimetype,
                folder_id = dossier_id
            )
            
            db.session.add(document)
            saved.append(filename)
                
        db.session.commit()
        return {"message": "Document enrégistrer avec succès"}, 201
    
    @staticmethod
    def get_all_documents():
        query_text = request.args.get("q", "").strip()
        if not query_text:
            Documents = db.session.query(Document).join(Folder).limit(6)
        else:
            Documents = db.session.query(Document).join(Folder).filter(
                or_(
                    Folder.numero_dossier.ilike(f"%{query_text}%"),
                ),
            ).all()
        
        Document_data =[
        {
            "id": t.id,
            "filename": t.filename,
            "mimetype": t.mimetype,
            "folder": {
                "id": t.folder.id,
                "numero_dossier": t.folder.numero_dossier,
            },
        }for t in Documents
        ]
        return Document_data
    
    @staticmethod
    def view_document(doc_id):
        document = Document.query.get(doc_id)
        if not document:
            return {"message": "Document non trouvé", "status": 404}
        if not os.path.exists(document.filepath):
            return {"message": "Document manquant", "status": 404}
        
        return send_file(
            document.filepath,
            mimetype=document.mimetype,
            as_attachment=False
        )
            
    @staticmethod
    def delete_document(id):
        doc = Document.query.get(id)
        if not doc:
            return {"message": "Document non trouvé", "status": 404}
        
        db.session.delete(doc)
        db.session.commit()
        return {"message":"Document supprimé avec succès", "status":201}
    
    @staticmethod
    def update_file(id):
        doc = Document.query.get(id)
        if not doc:
           return {"message": "Aucun document ne correspond"}, 400
        # Upload de plusieurs documents liés à un dossier
        # Verification dossier
        dossier_id = request.form.get("folder_id")
        if dossier_id:
            doc.folder_id = dossier_id
            
        files = request.files.getlist("files")
        if files and files[0].filename != "":
            for file in files:
                if not files:
                    return {"message": "Aucun fichier envoyer"}, 400
                if not allowed_extension(file.filename, ALLOWED_EXTENSIONS):
                    return {"message": "Extension non autorisée"}, 400
                if not allowed_mime(file.mimetype, ALLOWED_MIMES_TYPE):
                    return {"message": "Type MIME non autorisé"}, 400
       
                filename = secure_filename(files.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                
                file.save(filepath)
                doc.filename = filename
                doc.filepath = filepath
                doc.mimetype = file.mimetype
                
        db.session.commit()
        print("folder_id:", dossier_id)
        print("files:", files)
        return {"message": "Document Modifié avec succès", "status": 204}