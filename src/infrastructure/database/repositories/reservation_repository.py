
from typing import Optional

from sqlalchemy.orm import Session

from ....application.interfaces.repository import ReservationRepositoryInterface
from ....domain.entities.reservation import Reservation
from ....domain.entities.user import User
from ....domain.value_objects.contact_info import ContactInfo
from ....domain.value_objects.time_slot import TimeSlot
from ..models import ReservationModel


class ReservationRepository(ReservationRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, reservation_id: int) -> Optional[Reservation]:
        model = (
            self._session.query(ReservationModel)
            .filter(ReservationModel.reservation_id == reservation_id)
            .first()
        )

        if not model:
            return None

        return self._model_to_entity(model)

    def find_all(self) -> list[Reservation]:
        models = self._session.query(ReservationModel).all()
        return [self._model_to_entity(model) for model in models]

    def find_by_office_and_time(self, office_id: int, time_slot: TimeSlot) -> list[Reservation]:
        models = (
            self._session.query(ReservationModel)
            .filter(
                ReservationModel.office_id == office_id,
                ReservationModel.start_time < time_slot.end_time,
                ReservationModel.end_time > time_slot.start_time,
                ReservationModel.status.in_(["pending", "confirmed"]),
            )
            .all()
        )

        return [self._model_to_entity(model) for model in models]

    def save(self, reservation: Reservation) -> Reservation:
        if reservation.reservation_id:
            model = (
                self._session.query(ReservationModel)
                .filter(ReservationModel.reservation_id == reservation.reservation_id)
                .first()
            )

            if model:
                self._update_model_from_entity(model, reservation)
            else:
                model = self._entity_to_model(reservation)
                self._session.add(model)
        else:
            model = self._entity_to_model(reservation)
            self._session.add(model)

        self._session.commit()
        self._session.refresh(model)

        return self._model_to_entity(model)

    def delete(self, reservation_id: int) -> bool:
        model = (
            self._session.query(ReservationModel)
            .filter(ReservationModel.reservation_id == reservation_id)
            .first()
        )

        if not model:
            return False

        self._session.delete(model)
        self._session.commit()

        return True

    @staticmethod
    def _model_to_entity(model: ReservationModel) -> Reservation:
        return Reservation(
            reservation_id=model.reservation_id,  # type: ignore
            office_id=model.office_id,  # type: ignore
            status=model.status,  # type: ignore
            created_at=model.created_at,  # type: ignore
            user=User(
                user_id=None,  # User ID not stored in this simple model
                name=model.user_name,  # type: ignore
                contact_info=ContactInfo(
                    email=model.user_email,  # type: ignore
                    phone=model.user_phone,  # type: ignore
                ),
            ),
            time_slot=TimeSlot(
                start_time=model.start_time,  # type: ignore
                end_time=model.end_time,  # type: ignore
            ),
        )

    @staticmethod
    def _entity_to_model(reservation: Reservation) -> ReservationModel:
        return ReservationModel(
            reservation_id=reservation.reservation_id,
            office_id=reservation.office_id,
            user_name=reservation.user.name,
            user_email=reservation.user.contact_info.email,
            user_phone=reservation.user.contact_info.phone,
            start_time=reservation.time_slot.start_time,
            end_time=reservation.time_slot.end_time,
            status=reservation.status.value,
            created_at=reservation.created_at,
        )

    @staticmethod
    def _update_model_from_entity(model: ReservationModel, entity: Reservation) -> None:
        model.office_id = entity.office_id  # type: ignore
        model.user_name = entity.user.name  # type: ignore
        model.user_email = entity.user.contact_info.email  # type: ignore
        model.user_phone = entity.user.contact_info.phone  # type: ignore
        model.start_time = entity.time_slot.start_time  # type: ignore
        model.end_time = entity.time_slot.end_time  # type: ignore
        model.status = entity.status.value  # type: ignore
