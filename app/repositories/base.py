from typing import Generic, TypeVar, Type, List
from sqlalchemy.orm import Session
from sqlalchemy import select

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def get(self, id: int) -> T:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def list(self) -> List[T]:
        return self.db.query(self.model).all()

    def add(self, obj: T):
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: T):
        self.db.delete(obj)
        self.db.commit()

from .base import BaseRepository
from ..models import Category

class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db: Session):
        super().__init__(db, Category)

    def get_children_count(self, category_id: int) -> int:
        return self.db.query(Category).filter(Category.parent_id == category_id).count()

    def get_root_categories(self):
        return self.db.query(Category).filter(Category.parent_id == None).all()
