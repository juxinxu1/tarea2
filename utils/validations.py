import re
import filetype

# Validar nombre del organizador
def validate_nombre(nombre):
    return bool(nombre) and 1 <= len(nombre.strip()) <= 200

# Validar email con patrón estándar
def validate_email(email):
    return (
        bool(email)
        and len(email.strip()) <= 100
        and re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email.strip())
    )

# Validar número de celular en formato chileno: +56912345678 (opcional)
def validate_telefono(telefono):
    return not telefono or re.match(r"^\+569\d{8}$", telefono)

# Validar red social y su identificador si se elige "otra"
def validate_contacto(contactar_por, id_contacto):
    if contactar_por == "otra":
        return bool(id_contacto) and 4 <= len(id_contacto.strip()) <= 50
    return True

# Validar campo datetime-local (formato: YYYY-MM-DDTHH:MM)
def validate_datetime(dt):
    return bool(dt) and re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$", dt)

# Validar que el término (si existe) sea posterior al inicio
def validate_termino(inicio, termino):
    if not termino:
        return True
    return termino > inicio

# Validar el tema, y si es "otro", que tenga glosa válida
def validate_tema(tema, glosa_otro):
    if tema == "otro":
        return bool(glosa_otro) and 3 <= len(glosa_otro.strip()) <= 15
    return tema in [
        "música", "deporte", "ciencias", "religión", "política", "tecnología",
        "juegos", "baile", "comida", "otro"
    ]

# Validar fotos: al menos una, máximo 5, y tipos de imagen válidos
def validate_fotos(files):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}

    if not files or not (1 <= len(files) <= 5):
        return False

    for f in files:
        if not f or f.filename.strip() == "":
            return False
        guess = filetype.guess(f)
        if not guess or guess.extension not in ALLOWED_EXTENSIONS or guess.mime not in ALLOWED_MIMETYPES:
            return False

    return True

# Validación final del formulario completo
def validate_activity_form(data, files):
    return (
        validate_nombre(data.get("organizador_nombre")) and
        validate_email(data.get("organizador_email")) and
        validate_telefono(data.get("organizador_telefono")) and
        validate_contacto(data.get("contactar_por"), data.get("otro_contacto")) and
        validate_datetime(data.get("inicio")) and
        validate_termino(data.get("inicio"), data.get("termino")) and
        validate_tema(data.get("tema"), data.get("otro_tema")) and
        validate_fotos(files.getlist("fotos[]"))
    )
