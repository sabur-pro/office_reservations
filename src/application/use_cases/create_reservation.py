
from ...domain.entities.reservation import Reservation
from ...domain.entities.user import User
from ...domain.exceptions.domain_exceptions import (
    OfficeNotFoundError,
    ReservationConflictError,
)
from ...domain.value_objects.contact_info import ContactInfo
from ...domain.value_objects.time_slot import TimeSlot
from ..dto.reservation_dto import ReservationDTO
from ..interfaces.notification import NotificationData, NotificationServiceInterface
from ..interfaces.repository import (
    OfficeRepositoryInterface,
    ReservationRepositoryInterface,
)


class CreateReservationUseCase:
    def __init__(
        self,
        office_repository: OfficeRepositoryInterface,
        reservation_repository: ReservationRepositoryInterface,
        notification_service: NotificationServiceInterface,
    ) -> None:
        self._office_repository = office_repository
        self._reservation_repository = reservation_repository
        self._notification_service = notification_service

    def execute(
        self,
        office_id: int,
        user_name: str,
        user_email: str,
        user_phone: str,
        time_slot: TimeSlot,
    ) -> ReservationDTO:
        office = self._office_repository.get_by_id(office_id)
        if not office:
            raise OfficeNotFoundError(office_id)

        conflicting_reservations = self._reservation_repository.find_by_office_and_time(
            office_id, time_slot
        )

        if conflicting_reservations:
            conflict = conflicting_reservations[0]
            raise ReservationConflictError(
                office_id=office_id,
                conflicting_user=conflict.user.name,
                end_time=conflict.time_slot.end_time.strftime("%Y-%m-%d %H:%M"),
                conflicting_email=conflict.user.contact_info.email,
                conflicting_phone=conflict.user.contact_info.phone,
            )

        contact_info = ContactInfo(email=user_email, phone=user_phone)
        user = User(user_id=None, name=user_name, contact_info=contact_info)

        reservation = Reservation(
            office_id=office_id,
            user=user,
            time_slot=time_slot,
        )

        reservation.confirm()

        saved_reservation = self._reservation_repository.save(reservation)

        notification_data = NotificationData(
            recipient_name=user_name,
            recipient_email=user_email,
            recipient_phone=user_phone,
            office_id=office_id,
            office_name=office.name,
            start_time=time_slot.start_time.strftime("%Y-%m-%d %H:%M"),
            end_time=time_slot.end_time.strftime("%Y-%m-%d %H:%M"),
            reservation_id=saved_reservation.reservation_id or 0,
        )

        self._notification_service.send_all(notification_data)

        return ReservationDTO(
            reservation_id=saved_reservation.reservation_id,
            office_id=office_id,
            office_name=office.name,
            user_name=user_name,
            user_email=user_email,
            user_phone=user_phone,
            start_time=time_slot.start_time.strftime("%Y-%m-%d %H:%M"),
            end_time=time_slot.end_time.strftime("%Y-%m-%d %H:%M"),
            status=saved_reservation.status.value,
            created_at=saved_reservation.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        )
