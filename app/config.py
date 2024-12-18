import os

# Puedes usar variables de entorno o valores predeterminados
secret_key = os.getenv("SECRET_KEY", "your-secret-key")  # Reemplaza con una clave segura
jwt_algorithm = "HS256"  # Algoritmo para firmar el token JWT
