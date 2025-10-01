from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..repositories.order import OrderRepository
from ..models import Product

class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.order_repo = OrderRepository(db)

    def add_product(self, order_id: int, product_id: int, quantity: int):
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError("Product not found")
        if product.quantity_in_stock < quantity:
            raise ValueError("Not enough stock")
        product.quantity_in_stock -= quantity
        self.order_repo.add_product_to_order(order_id, product_id, quantity)
        self.db.commit()

    def get_top_products_last_month(self):
        last_month = datetime.now() - timedelta(days=30)
        return (
            self.db.query(
                Product.name.label("product_name"),
:
                Category.name.label("category_name"),
                func.sum(OrderItem.quantity).label("total_sold")
            )
            .join(OrderItem.product)
            .join(Product.category)
            .join(OrderItem.order)
            .filter(Order.created_at >= last_month.strftime('%Y-%m-%d'))
            .group_by(Product.id)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(5)
        )
