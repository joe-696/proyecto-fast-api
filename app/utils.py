import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Cargar las claves secretas y configuración desde variables de entorno (para mayor seguridad)
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")  # Reemplaza con tu clave secreta
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Duración del token (en minutos)

# Inicializar contexto para la encriptación de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para verificar si la contraseña proporcionada es correcta
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si la contraseña proporcionada es correcta comparando con el hash.
    """
    return pwd_context.verify(plain_password, hashed_password)

# Función para obtener el hash de la contraseña
def get_password_hash(password: str) -> str:
    """
    Genera un hash de la contraseña proporcionada.
    """
    return pwd_context.hash(password)

# Función para crear un token de acceso JWT
def create_access_token(data: dict) -> str:
    """
    Crea un token JWT con los datos proporcionados.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para decodificar el token JWT y obtener el payload
def decode_access_token(token: str) -> dict:
    """
    Decodifica un token JWT y retorna el payload.
    Si el token es inválido o ha expirado, devuelve None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Verifica si el token ha expirado, si no, retorna el payload.
        if datetime.utcfromtimestamp(payload.get("exp")) < datetime.utcnow():
            return None
        return payload
    except JWTError:
        return None
