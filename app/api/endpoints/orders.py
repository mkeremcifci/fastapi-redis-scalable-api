from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.redis import get_redis
from app.api import deps
from app.services.order_service import create_new_order
from app.schemas.order import OrderCreate

router = APIRouter()

@router.post("/")
async def create_order(
    order_data: OrderCreate,
    db: Session = Depends(deps.get_db),
    redis = Depends(get_redis),
    user_id: int
):
    return await create_new_order(db, redis, user_id, order_data)