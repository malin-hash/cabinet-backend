from Extensions import db

class Document(db.Model):
    __tablename__="documents"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    mimetype = db.Column(db.String(100))
    folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'), nullable=False)
    
    