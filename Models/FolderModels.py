from Extensions import db

class Folder(db.Model):
    __tablename__ = "folders"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=True)
    numero_dossier = db.Column(db.String(6), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    avocat_id = db.Column(db.Integer, db.ForeignKey('avocats.id'), nullable=False)
    affaire_id = db.Column(db.Integer, db.ForeignKey('affaires.id'), nullable=False)
    is_archive = db.Column(db.Boolean, default=False)
    
    factures = db.relationship('Facture', backref='folder', lazy=True, cascade="all, delete-orphan")
    documents = db.relationship('Document', backref='folder', lazy=True, cascade="all, delete-orphan")
    notes = db.relationship('Note', backref='folder', lazy=True, cascade="all, delete-orphan")
    
    