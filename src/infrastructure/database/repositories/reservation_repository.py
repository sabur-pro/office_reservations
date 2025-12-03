from typing import List, Optional

from sqlalchemy.orm import Session

from ....application.interfaces.repository import ReservationRepositoryInterface
from ....domain.entities.reservation import Reservation, ReservationStatus
from ....domain.entities.user import User
from ....domain.value_objects.contact_info import ContactInfo
from ....domain.value_objects.time_slot import TimeSlot
from ..models import ReservationModel


class ReservationRepository(ReservationRepositoryInterface):
    def __init__(self, session: Session) -> None:
        self._session = session
    
    def find_by_id(self, reservation_id: int) -> Optional[Reservation]:
        model = self._session.query(ReservationModel).filter(
            ReservationModel.reservation_id == reservation_id
        ).first()
        
        if not model:
            return None
        
        return self._model_to_entity(model)
    
    def find_all(self) -> List[Reservation]:
        models = self._session.query(ReservationModel).all()
        return [self._model_to_entity(model) for model in models]
    
    def find_by_office_and_time(
        self,
        office_id: int,
        time_slot: TimeSlot
    ) -> List[Reservation]:
        models = self._session.query(ReservationModel).filter(
            ReservationModel.office_id == office_id,
            ReservationModel.start_time < time_slot.end_time,
            ReservationModel.end_time > time_slot.start_time,
            ReservationModel.status.in_(['pending', 'confirmed'])
        ).all()
        
        return [self._model_to_entity(model) for model in models]
    
    def save(self, reservation: Reservation) -> Reservation:
        if reservation.reservation_id:
            model = self._session.query(ReservationModel).filter(
                ReservationModel.reservation_id == reservation.reservation_id
            ).first()
            
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
        model = self._session.query(ReservationModel).filter(
            ReservationModel.reservation_id == reservation_id
        ).first()
        
        if not model:
            return False
        
        self._session.delete(model)
        self._session.commit()
        
        return True
    
    @staticmethod
    def _model_to_entity(model: ReservationModel) -> Reservation:
        contact_info = ContactInfo(
            email=model.user_email,
            phone=model.user_phone
        )
        
        user = User(
            user_id=None,
            name=model.user_name,
            contact_info=contact_info
        )
        
        time_slot = TimeSlot(
            start_time=model.start_time,
            end_time=model.end_time
        )
        
        return Reservation(
            reservation_id=model.reservation_id,
            office_id=model.office_id,
            user=user,
            time_slot=time_slot,
            status=ReservationStatus(model.status),
            created_at=model.created_at
        )
    
    @staticmethod
    def _entity_to_model(entity: Reservation) -> ReservationModel:
        return ReservationModel(
            reservation_id=entity.reservation_id,
            office_id=entity.office_id,
            user_name=entity.user.name,
            user_email=entity.user.contact_info.email,
            user_phone=entity.user.contact_info.phone,
            start_time=entity.time_slot.start_time,
            end_time=entity.time_slot.end_time,
            status=entity.status.value,
            created_at=entity.created_at
        )
    
    @staticmethod
    def _update_model_from_entity(
        model: ReservationModel,
        entity: Reservation
    ) -> None:
        model.office_id = entity.office_id
        model.user_name = entity.user.name
        model.user_email = entity.user.contact_info.email
        model.user_phone = entity.user.contact_info.phone
        model.start_time = entity.time_slot.start_time
        model.end_time = entity.time_slot.end_time
        model.status = entity.status.value
