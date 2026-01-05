from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import signal
import sys
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()
DATABASE_URL = settings.DATABASE_URL
engine = None
SessionLocal = None

def init_db():
    # Initialize database engine, session factory, and validate database connectivity.
    
    global engine, SessionLocal

    if not DATABASE_URL:
        print("DATABASE_URL is missing")
        sys.exit(1)

    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,   # handles stale connections
        future=True
    )

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    _validate_db_connection()

def _validate_db_connection():
    # Validate database connectivity.

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database connection successful")
    except SQLAlchemyError as exc:
        print(f"Failed to connect to database: {exc}")
        sys.exit(1)

def get_db():
    # FastAPI dependency that provides a DB session.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def shutdown_db():
    # Dispose database engine on shutdown.
    if engine:
        engine.dispose()
        print("Database connection closed")

