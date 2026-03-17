from Extensions import db

class Facture(db.Model):
    __tablename__ = "factures"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=True)
    FraisOuverture = db.Column(db.Float, nullable=True)
    FraisFirstInstance = db.Column(db.Float, nullable=True)
    FraisAppel = db.Column(db.Float, nullable=True)
    FraisCassation = db.Column(db.Float, nullable=True)
    FraisIncident = db.Column(db.Float, nullable=True)
    FraisFinProcedure = db.Column(db.Float, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'), nullable=False)
    
    
    