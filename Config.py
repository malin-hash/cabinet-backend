import os
from datetime import timedelta

SECRET_KEY = "super-secret"
JWT_SECRET_KEY = "jwt-secret-key"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
JWT_TOKEN_LOCATION = ["headers"]

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:VbtMFyOzWmQqlgZBpLpUtHmGjyisfnXB@mysql.railway.internal:3306/railway"
SQLALCHEMY_TRACK_MODIFICATIONS = False

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "pdf"}

ALLOWED_MIMES_TYPE = {
    "text/plain",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "image/jpeg",
    "image/jpg",
    "image/png",
    "application/pdf",
    
}

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads', 'documents')
   
    
