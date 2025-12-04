
from typing import Optional

from sqlalchemy.orm import Session

from ....application.interfaces.repository import OfficeRepositoryInterface
from ....domain.entities.office import Office
from ..models import OfficeModel


class OfficeRepository(OfficeRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, office_id: int) -> Optional[Office]:
        model = self._session.query(OfficeModel).filter(OfficeModel.office_id == office_id).first()

        if not model:
            return None

        return self._model_to_entity(model)

    def find_all(self) -> list[Office]:
        models = self._session.query(OfficeModel).all()
        return [self._model_to_entity(model) for model in models]

    def save(self, office: Office) -> Office:
        existing_model = (
            self._session.query(OfficeModel)
            .filter(OfficeModel.office_id == office.office_id)
            .first()
        )

        if existing_model:
            existing_model.name = office.name  # type: ignore
            existing_model.capacity = office.capacity  # type: ignore
            existing_model.description = office.description  # type: ignore
        else:
            model = self._entity_to_model(office)
            self._session.add(model)

        self._session.commit()

        return office

    @staticmethod
    def _model_to_entity(model: OfficeModel) -> Office:
        return Office(
            office_id=model.office_id,  # type: ignore
            name=model.name,  # type: ignore
            capacity=model.capacity,  # type: ignore
            description=model.description,  # type: ignore
        )

    @staticmethod
    def _entity_to_model(entity: Office) -> OfficeModel:
        return OfficeModel(
            office_id=entity.office_id,
            name=entity.name,
            capacity=entity.capacity,
            description=entity.description,
        )

