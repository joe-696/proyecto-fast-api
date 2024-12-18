from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app import models
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.config import settings  # Asegúrate de tener la clave secreta en settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# Función para obtener el usuario actual desde el token JWT
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = await db.execute(select(models.User).filter(models.User.username == username))
        user = user.scalars().first()
        if user is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user
