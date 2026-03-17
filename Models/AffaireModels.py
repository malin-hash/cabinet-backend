from Extensions import db

class Affaire(db.Model):
    __tablename__ = 'affaires'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    folders = db.relationship('Folder', backref='affaire', lazy=True, cascade="all, delete-orphan")
