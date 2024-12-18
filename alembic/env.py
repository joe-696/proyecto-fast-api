from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.database import engine, Base  # Asegúrate de que la URL de la base de datos esté correctamente configurada en database.py
import app.models  # Importa tus modelos para que Alembic pueda detectarlos

# Este es el objeto de configuración de Alembic, que proporciona acceso a los valores dentro del archivo .ini en uso
config = context.config

# Interpretar el archivo de configuración para la configuración de logging. Esta línea configura los loggers básicamente.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Agrega el objeto MetaData de tus modelos aquí para habilitar el soporte de 'autogenerate'
# Importando las tablas de tu base de datos
target_metadata = Base.metadata

# Función para ejecutar migraciones en modo offline
def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo 'offline'.

    Esto configura el contexto solo con una URL y no un Engine,
    aunque un Engine también es aceptable aquí. Al omitir la creación del Engine, ni siquiera necesitamos
    un DBAPI disponible. Las llamadas a context.execute() aquí emiten la cadena dada en la salida del script.
    """
    url = config.get_main_option("sqlalchemy.url")  # La URL de la base de datos tomada desde alembic.ini
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# Función para ejecutar migraciones en modo online
def run_migrations_online() -> None:
    """Ejecuta migraciones en modo 'online'.

    En este escenario necesitamos crear un Engine y asociar una conexión con el contexto.
    """
    # Crear el engine utilizando la configuración de alembic.ini
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Ejecutar las migraciones utilizando la conexión
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# Determinar si Alembic está en modo offline o online
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
