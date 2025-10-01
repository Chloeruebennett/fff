from typing import List
from sqlalchemy.orm import Session
from ..models import Order, OrderItem, Product

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, order_id: int) -> Order:
        return self.db.query(Order).filter(Order.id == order_id).first()

    def add_product_to_order(self, order_id: int, product_id: int, quantity: int):
        order = self.get_by_id(order_id)
        if not order:
            raise ValueError("Order not found")
        existing_item = self.db.query(OrderItem).filter_by(order_id=order_id, product_id=product_id).first()
        if existing_item:
            existing_item.quantity += quantity
        else:
            new_item = OrderItem(order_id=order_id, product_id=product_id, quantity=quantity)
            self.db.add(new_item)
        self.db.commit()

    def get_order_summary(self, order_id: int):
        return self.db.query(OrderItem).filter_by(order_id=order_id).all()
