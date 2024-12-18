from fastapi import FastAPI
#from fastapi.staticfiles import StaticFiles  # Agregar esta línea
from app.routers import posts, users  # Asegúrate de importar correctamente tus routers

app = FastAPI()

# Incluir las rutas de los usuarios con un prefijo '/users'
# El prefijo significa que las rutas de este router comenzarán con '/users', por ejemplo '/users/register'
app.include_router(users.router, prefix="/users", tags=["Users"])

# Incluir las rutas de los posts con un prefijo '/posts'
# Las rutas de este router comenzarán con '/posts', por ejemplo '/posts/me'
app.include_router(posts.router, prefix="/posts", tags=["Posts"])

# Servir archivos estáticos (como tu HTML)
#app.mount("/", StaticFiles(directory="static", html=True), name="static")