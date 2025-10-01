from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.order_service import OrderService
from app.schemas.order import AddProductRequest, OrderSummaryResponse
from app.models import Order

router = APIRouter()

@router.post("/orders/{order_id}/add-product")
def add_product(order_id: int, request: AddProductRequest, db: Session = Depends(get_db)):
    service = OrderService(db)
    try:
        service.add_product(order_id, request.product_id, request.quantity)
        return {"detail": "Product added/updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/orders/{order_id}/summary", response_model=OrderSummaryResponse)
def get_order_summary(order_id: int, db: Session = Depends(get_db)):
    service = OrderService(db)
    order_items = service.get_order_summary(order_id)
    return {"order_id": order_id, "items": [{"product_name": item.product.name, "quantity": item.quantity} for item in order_items]}
