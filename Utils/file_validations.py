# Verification de l'extension
def allowed_extension(filename, allowed_extensions):
    return (
        '.' in filename and 
        filename.rsplit('.', 1)[1].lower() in allowed_extensions
    )
    
# Vérification du type Mime
def allowed_mime(mimetype, allowed_mimes):
    return mimetype in allowed_mimes