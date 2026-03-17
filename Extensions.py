from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Initialisation 
jwt = JWTManager()
db = SQLAlchemy()