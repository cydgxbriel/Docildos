from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import sys
from pathlib import Path

# Adicionar diretório pai ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

load_dotenv()

# Importar configuração centralizada
try:
    from app.config import config as backend_config
    DATABASE_URL = backend_config.database_url
except ImportError:
    # Fallback se config não estiver disponível
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://docildos:docildos_dev@localhost:5432/docildos_db"
    )

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

