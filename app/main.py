from fastapi import FastAPI
from .config import settings
from .database import engine, Base
from .routers import order, category, customer

app = FastAPI(title="E-Commerce API", prefix=settings.api_prefix)

Base.metadata.create_all(bind=engine)

app.include_router(order.router)
app.include_router(category.router)
app.include_router(customer.router)
