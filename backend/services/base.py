from typing import Type, TypeVar, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database.models import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseService:
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def create(self, obj_data: dict) -> ModelType:
        try:
            obj = self.model(**obj_data)
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Error creating {self.model.__name__}: {str(e)}")

    def read(self, obj_id: str) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.id == obj_id).first()

    def update(self, obj_id: str, update_data: dict) -> Optional[ModelType]:
        try:
            obj = self.db.query(self.model).filter(self.model.id == obj_id).first()
            if not obj:
                return None
            for key, value in update_data.items():
                setattr(obj, key, value)
            self.db.commit()
            self.db.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Error updating {self.model.__name__}: {str(e)}")

    def delete(self, obj_id: str) -> bool:
        try:
            obj = self.db.query(self.model).filter(self.model.id == obj_id).first()
            if not obj:
                return False
            self.db.delete(obj)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Error deleting {self.model.__name__}: {str(e)}")

    def list(self) -> List[ModelType]:
        return self.db.query(self.model).all()