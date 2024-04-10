from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union
import math
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.main.models.db.base_class import Base
from app.main import schemas, models

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
            self, db: Session, *, page: int = 0, per_page: int = 20, keyword: str, order: str = "desc",
            role_uuid: str = None, order_field: str = "date_added"
    ) -> schemas.DataList:

        record_query = db.query(models.User).filter(models.User.status != models.UserStatusType.DELETED)

        if role_uuid:
            record_query = record_query.filter(
                or_(models.User.role_uuid == role_uuid, models.User.creation_assigned_role_uuid == role_uuid))

        record_query = record_query.filter(or_(
            models.User.email.ilike('%' + str(keyword) + '%'),
            models.User.firstname.ilike('%' + str(keyword) + '%'),
            models.User.lastname.ilike('%' + str(keyword) + '%'),
        ))

        total = record_query.count()

        if order in ["asc", "ASC"]:
            record_query = record_query.order_by(getattr(models.User, order_field).asc())

        if order in ["desc", "DESC"]:
            record_query = record_query.order_by(getattr(models.User, order_field).desc())

        result = record_query.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.DataList(
            total=total,
            pages=math.ceil(total / per_page),
            current_page=page,
            per_page=per_page,
            data=result
        )

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self,
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
