from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import logging
from urllib.parse import quote_plus

# Load env variables
from dotenv import load_dotenv
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv(dotenv_path="secrets.env")

# Dynamically build DATABASE_URL from env
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))  # URL encode the password
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# Log the environment variables (excluding password)
logger.info(f"DB_USER: {DB_USER}")
logger.info(f"DB_HOST: {DB_HOST}")
logger.info(f"DB_NAME: {DB_NAME}")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
logger.info(f"Database URL: postgresql://{DB_USER}:****@{DB_HOST}/{DB_NAME}")

# Import Base to get target_metadata
from models import Base
target_metadata = Base.metadata

# Alembic config
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=DATABASE_URL,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
