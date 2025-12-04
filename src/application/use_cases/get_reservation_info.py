from ...domain.exceptions.domain_exceptions import OfficeNotFoundError
from ...domain.value_objects.time_slot import TimeSlot
from ..dto.reservation_dto import ReservationInfoDTO
from ..interfaces.repository import (
    OfficeRepositoryInterface,
    ReservationRepositoryInterface,
)


class GetReservationInfoUseCase:
    def __init__(
        self,
        office_repository: OfficeRepositoryInterface,
        reservation_repository: ReservationRepositoryInterface,
    ) -> None:
        self._office_repository = office_repository
        self._reservation_repository = reservation_repository

    def execute(self, office_id: int, time_slot: TimeSlot) -> ReservationInfoDTO:
        office = self._office_repository.get_by_id(office_id)
        if not office:
            raise OfficeNotFoundError(office_id)

        reservations = self._reservation_repository.find_by_office_and_time(office_id, time_slot)

        if not reservations:
            return ReservationInfoDTO(
                office_id=office_id,
                office_name=office.name,
                is_occupied=False,
                message=(
                    f"Office {office_id} ({office.name}) is free during "
                    f"{time_slot.start_time.strftime('%Y-%m-%d %H:%M')} - "
                    f"{time_slot.end_time.strftime('%H:%M')}"
                ),
            )

        reservation = reservations[0]

        return ReservationInfoDTO(
            office_id=office_id,
            office_name=office.name,
            is_occupied=True,
            occupied_by=reservation.user.name,
            occupant_email=reservation.user.contact_info.email,
            occupant_phone=reservation.user.contact_info.phone,
            from_time=reservation.time_slot.start_time.strftime("%Y-%m-%d %H:%M"),
            until_time=reservation.time_slot.end_time.strftime("%Y-%m-%d %H:%M"),
            message=(
                f"Office {office_id} ({office.name}) is occupied by "
                f"{reservation.user.name} "
                f"({reservation.user.contact_info.email}, "
                f"{reservation.user.contact_info.phone}) "
                f"from {reservation.time_slot.start_time.strftime('%Y-%m-%d %H:%M')} "
                f"until {reservation.time_slot.end_time.strftime('%Y-%m-%d %H:%M')}"
            ),
        )
