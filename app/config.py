import os


MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql-colegiodh.alwaysdata.net")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "colegiodh_")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "cris123456.")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "colegiodh_automatizaciondh")

JWT_SECRET = os.getenv("JWT_SECRET", "cambia-esta-clave-en-produccion")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}
MAX_FILE_SIZE = 10 * 1024 * 1024
