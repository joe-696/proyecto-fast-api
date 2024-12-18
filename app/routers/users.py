from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas, utils
from app.database import get_db

router = APIRouter()

# Ruta para registrar a un nuevo usuario
@router.post("/register", response_model=schemas.UserResponse)
async def register_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).filter(models.User.username == user.username))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = utils.get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

# Ruta para iniciar sesión y obtener el token JWT
@router.post("/login")
async def login_user(user: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).filter(models.User.username == user.username))
    existing_user = result.scalars().first()
    if not existing_user or not utils.verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = utils.create_access_token(data={"sub": existing_user.username})
    return {"access_token": access_token, "token_type": "bearer"}
