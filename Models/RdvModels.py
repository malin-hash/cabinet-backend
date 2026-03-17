from Extensions import db

class Rdv(db.Model):
    __tablename__ = 'rdvs'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    heureDebut = db.Column(db.Time, nullable=False)
    heureFin = db.Column(db.Time, nullable=False)
    statut = db.Column(db.Boolean, default=False)
    subject = db.Column(db.String(200), nullable=False)
    affaire_id = db.Column(db.Integer, db.ForeignKey('affaires.id'), nullable=True)

    def get_time_end(self):
        return self.heureFin