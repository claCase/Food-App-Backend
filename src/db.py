from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base


SQLALCHEMY_DATABASE_URL = "sqlite+pysqlite:///recipes.db"

Base = declarative_base()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
