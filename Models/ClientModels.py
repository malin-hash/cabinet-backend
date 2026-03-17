from Extensions import db

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phoneNumber = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    nationality = db.Column(db.String(150), nullable=False)
    profession = db.Column(db.String(150), nullable=False) 
    updated_at = db.Column(db.DateTime)
    folders = db.relationship('Folder', backref='client', lazy=True, cascade="all, delete-orphan")
    
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'firstname': self.firstname,
            'address': self.address,
            'genre': self.genre,
            'email': self.email,
            'profession': self.profession,
            'phoneNumber': self.phoneNumber,
            'nationality': self.nationality
        }
    