from typing import Generator
from app.core.database import SessionLocal
from app.core.redis import get_redis

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()