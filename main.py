from fastapi import FastAPI
from app.api.endpoints.orders import router as order_router



app = FastAPI(title="Order Management API")
app.include_router(order_router, prefix="/orders", tags=["Orders"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Order Management API"}