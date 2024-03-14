from sqlmodel import Session, create_engine, select, delete
from .db import BaseDBModel
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DBManager:
    def __init__(self, engine_uri: str):
        self.engine = create_engine(engine_uri)
        self.session = Session(self.engine)

    def create_db_and_tables(self):
        BaseDBModel.metadata.create_all(self.engine)

    def upsert(self, model: BaseDBModel):
        # check if the model exists, update else add
        model_class = type(model)
        current_model = self.session.exec(
            select(model_class).where(model_class.id == model.id)).first()
        if current_model:
            model.updated_at = datetime.now()
            self.session.update(model)
        else:
            self.session.add(model)
        self.session.commit()

    def _model_to_dict(self, model_obj):
        return {col.name: getattr(model_obj, col.name) for col in model_obj.__table__.columns}

    def get(self, row_id: int, model_class: BaseDBModel, return_json: bool = False):
        statement = select(model_class).where(model_class.id == row_id)
        if return_json:
            return [self._model_to_dict(row) for row in self.session.exec(statement).all()]
        else:
            return self.session.exec(statement).all()

    def get_all(self, model_class: BaseDBModel, return_json: bool = False):
        statement = select(model_class)
        if return_json:
            return [self._model_to_dict(row) for row in self.session.exec(statement).all()]
        else:
            return self.session.exec(statement).all()

    def delete(self, row_id: int, model_class: BaseDBModel):
        row = self.session.exec(select(model_class).where(
            model_class.id == row_id)).one_or_none()
        if row:
            self.session.delete(row)
            self.session.commit()
        else:
            print(f"Row with id {row_id} not found")
            logger.info("Row with id %s not found", row_id)

    def delete_all(self, model_class: BaseDBModel):
        result = self.session.exec(delete(model_class))
        self.session.commit()
        logger.info("All rows in %s (%s) deleted", model_class, result.rowcount)
