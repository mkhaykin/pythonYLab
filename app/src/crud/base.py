from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel

from app.src import models
from app.src import schemas


class CRUDBase:
    def __init__(self, model, name=""):
        self.__model = model
        self.__name = name

    @property
    def model(self):
        return self.__model

    @property
    def name(self):
        return self.__name

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def get(self, obj_id: UUID, db: Session, raise_404: bool = False):
        # TODO check exists
        # query = db.query(self.model).filter(self.model.id == obj_id)
        # db_obj = query.first()
        # if not db_obj:
        #     raise Exception(404, f"{self.name} not found")
        # return db_obj
        return db.query(self.model).filter(self.model.id == obj_id).first()

    def create(self, obj: BaseModel, db: Session):
        db_obj = self.model(**obj.model_dump())
        try:
            db.add(db_obj)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise Exception(409, f"the {self.name} is duplicated")
        except Exception:
            db.rollback()
            raise Exception(424, f"DB error while creating {self.name}")

        db.refresh(db_obj)
        return db_obj

    def update(self, obj_id: UUID, obj: BaseModel, db: Session):
        # FIXME use self.get(obj_id)
        # db_obj = self.get(obj_id, db)
        query = db.query(self.model).filter(self.model.id == obj_id)
        db_obj = query.first()
        if not db_obj:
            raise Exception(404, f"{self.name} not found")

        try:
            for column, value in obj.model_dump(exclude_unset=True).items():
                setattr(db_obj, column, value)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise Exception(409, f"the {self.name} is duplicated")
        except Exception:
            db.rollback()
            raise Exception(424, f"DB error while update {self.name}")

        db.refresh(db_obj)
        return db_obj

    def delete(self, obj_id: UUID, db: Session):
        # TODO use self.get(obj_id, db)
        # db_obj = self.get(obj_id, db)
        db_obj = db.query(self.__model).filter(self.__model.id == obj_id).first()
        if not db_obj:
            raise Exception(404, f"{self.name} not found")

        try:
            db.delete(db_obj)
            db.commit()
        except Exception:
            db.rollback()
            raise Exception(424, f"DB error while deleting {self.name}")

        return