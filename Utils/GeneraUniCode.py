import random
import string
from Models import Folder

def generate_code(length=6):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.sample(characters, length))
    
def generate_unique_code():
    while True:
        code = generate_code()
        existing_folder = Folder.query.filter_by(numero_dossier=code).first()
        if not existing_folder:
            return code