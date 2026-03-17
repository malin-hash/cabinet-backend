from Extensions import db

class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'), nullable=False)
    
    
    