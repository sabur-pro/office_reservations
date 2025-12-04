
from ...domain.exceptions.domain_exceptions import OfficeNotFoundError
from ...domain.value_objects.time_slot import TimeSlot
from ..dto.reservation_dto import AvailabilityDTO, ConflictingReservationDTO
from ..interfaces.repository import (
    OfficeRepositoryInterface,
    ReservationRepositoryInterface,
)


class CheckAvailabilityUseCase:
    def __init__(
        self,
        office_repository: OfficeRepositoryInterface,
        reservation_repository: ReservationRepositoryInterface,
    ) -> None:
        self._office_repository = office_repository
        self._reservation_repository = reservation_repository

    def execute(self, office_id: int, time_slot: TimeSlot) -> AvailabilityDTO:
        office = self._office_repository.get_by_id(office_id)
        if not office:
            raise OfficeNotFoundError(office_id)

        conflicting_reservations = self._reservation_repository.find_by_office_and_time(
            office_id, time_slot
        )

        conflicts: list[ConflictingReservationDTO] = []
        for reservation in conflicting_reservations:
            conflicts.append(
                ConflictingReservationDTO(
                    user_name=reservation.user.name,
                    user_email=reservation.user.contact_info.email,
                    user_phone=reservation.user.contact_info.phone,
                    start_time=reservation.time_slot.start_time.strftime("%Y-%m-%d %H:%M"),
                    end_time=reservation.time_slot.end_time.strftime("%Y-%m-%d %H:%M"),
                )
            )

        is_available = len(conflicts) == 0

        if is_available:
            message = (
                f"Office {office_id} ({office.name}) is available "
                f"from {time_slot.start_time.strftime('%Y-%m-%d %H:%M')} "
                f"to {time_slot.end_time.strftime('%H:%M')}"
            )
        else:
            message = (
                f"Office {office_id} ({office.name}) is NOT available. "
                f"Found {len(conflicts)} conflicting reservation(s)."
            )

        return AvailabilityDTO(
            office_id=office_id,
            office_name=office.name,
            is_available=is_available,
            requested_start_time=time_slot.start_time.strftime("%Y-%m-%d %H:%M"),
            requested_end_time=time_slot.end_time.strftime("%Y-%m-%d %H:%M"),
            conflicting_reservations=conflicts,
            message=message,
        )
