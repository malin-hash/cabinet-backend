import re
from datetime import datetime, date

def validate_text(value: str) -> bool:
    # Lettre Uniquement (accents autorisés)
    # Ne commence pas par un chiffre
    # Minimum 2 caractères
    if not value:
        return False
    
    value = value.strip()
    pattern = r"^[^\W\d_]+[\w -]{2,}$"
    return re.fullmatch(pattern, value) is not None
    
def validate_address(value: str) -> bool:
    # Lettre Uniquement (accents autorisés)
    # Ne commence pas par un chiffre
    # Minimum 2 caractères
    if not value:
        return False
    
    value = value.strip()
    pattern = r"^[\w]+[\w .,]{2,}$"
    return re.fullmatch(pattern, value) is not None
    
def validate_email(email: str) -> bool:
    if not email:
        return False
    
    email = email.strip().lower()
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return re.fullmatch(pattern, email) is not None
    
def validate_number(value: int) -> bool:
    if not value:
        return False
    pattern = r"^\d{8,}"
    return re.fullmatch(pattern, value) is not None

def validate_password(value: str) -> bool:
    if not value:
        return False
    value = value.strip()
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9]).{12,}$"
    return re.fullmatch(pattern, value) is not None

def validate_birth_date(value: str, min_age = 18) -> bool:
    if not value:
        return False
        
    try:
        birth_date = datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return False
        
    today = date.today()
    
    if birth_date > today:
        return False
    
    age = today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )
    
    return age >= min_age
    