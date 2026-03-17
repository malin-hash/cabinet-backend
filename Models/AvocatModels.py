from Extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Avocat(db.Model):
    __tablename__ = "avocats"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nationality = db.Column(db.String(150), nullable=False)
    genre = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    function = db.Column(db.String(50), nullable=False)
    phoneNumber = db.Column(db.Integer, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    folders = db.relationship('Folder', backref='avocat', lazy=True, cascade="all, delete-orphan")
    # Hash method (Password Hash)
    def set_password(self, mdp):
        passwords = str(mdp)
        self.password = generate_password_hash(passwords)
        
    # Check method (Password Verify)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'firstname': self.firstname,
            'address': self.address,
            'nationality': self.nationality,
            'phoneNumber': self.phoneNumber,
            'email': self.email,
            'function': self.function,
            'genre': self.genre,
            'is_admin': self.is_admin
        }