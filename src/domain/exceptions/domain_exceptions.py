

from typing import Any, Optional


class DomainError(Exception):
    def __init__(self, message: str, details: Optional[dict] = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class InvalidTimeSlotError(DomainError):
    def __init__(self, message: str = "Invalid time slot", **kwargs: Any) -> None:
        super().__init__(message, kwargs)


class OfficeNotAvailableError(DomainError):
    def __init__(self, office_id: int, message: Optional[str] = None, **kwargs: Any) -> None:
        msg = message or f"Office {office_id} is not available"
        details = {"office_id": office_id, **kwargs}
        super().__init__(msg, details)


class OfficeNotFoundError(DomainError):
    def __init__(self, office_id: int) -> None:
        super().__init__(f"Office with ID {office_id} not found", {"office_id": office_id})


class ReservationConflictError(DomainError):
    def __init__(self, office_id: int, conflicting_user: str, end_time: str, **kwargs: Any) -> None:
        message = f"Office {office_id} is occupied by {conflicting_user} until {end_time}"
        details = {
            "office_id": office_id,
            "conflicting_user": conflicting_user,
            "end_time": end_time,
            **kwargs,
        }
        super().__init__(message, details)


class ReservationNotFoundError(DomainError):
    def __init__(self, reservation_id: int) -> None:
        super().__init__(
            f"Reservation with ID {reservation_id} not found", {"reservation_id": reservation_id}
        )
