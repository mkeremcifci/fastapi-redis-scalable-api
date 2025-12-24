from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.product import Product
from redis import Redis
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.order import OrderCreate

async def create_new_order(db: Session, redis_client: Redis, user_id: int, order_data: OrderCreate):
    try:
        new_order = Order(
            user_id=user_id,
            status="pending",
        )
        db.add(new_order)
        db.flush()

        total_price = 0

        for item in order_data.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
            
            total_price += product.price * item.quantity
        
        db.commit()
        db.refresh(new_order)

        await redis_client.set(f"last_order_user_{user_id}", new_order.id, ex=3600)

        return new_order
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create order") from e
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") from e