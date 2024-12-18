from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import schemas, models, utils  # Asegúrate de importar modelos y utilidades correctamente
from app.database import get_db
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import SQLAlchemyError
import logging


# Usar OAuth2PasswordBearer para obtener el token desde los encabezados
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()

# Dependencia para obtener el usuario actual desde el token
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    # Decodificar el token usando la función que tienes en utils
    payload = utils.decode_access_token(token)

    # Si el token no es válido o no se puede decodificar, lanzar error 401
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Extraer el nombre de usuario (sub) desde el payload del token
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Buscar al usuario en la base de datos
    result = await db.execute(select(models.User).filter(models.User.username == username))
    user = result.scalars().first()

    # Si no se encuentra el usuario, lanzar error 401
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


# Ruta protegida que requiere autenticación
@router.get("/me", response_model=schemas.UserResponse)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


# Ruta para crear un nuevo post
@router.post("/", response_model=schemas.PostResponse)
async def create_post(
    post: schemas.PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_post = models.Post(
        title=post.title, content=post.content, owner_id=current_user.id
    )
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post


# Ruta pública para obtener todas las publicaciones
@router.get("/", response_model=list[schemas.PostResponse], tags=["Posts"])
async def get_all_posts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Post))
    posts = result.scalars().all()
    return posts


@router.get("/search", response_model=list[schemas.PostResponse], tags=["Posts"])
async def search_posts(title: str, db: AsyncSession = Depends(get_db)):
    """
    Buscar publicaciones por título.
    El parámetro 'title' se usa para buscar títulos que contengan el término dado.
    """
    # Usamos 'ilike' para buscar el título
    result = await db.execute(select(models.Post).filter(models.Post.title.ilike(f'%{title}%')))

    # Obtener los posts que coinciden con la búsqueda
    posts = result.scalars().all()

    # Si es necesario, conviértelo en un formato adecuado para Pydantic (lista de dicts)
    return posts  # FastAPI convertirá automáticamente las instancias de Post a JSON
