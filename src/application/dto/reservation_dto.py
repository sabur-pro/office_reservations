from dataclasses import dataclass
from typing import Optional


@dataclass
class ReservationDTO:
    office_id: int
    office_name: str
    user_name: str
    user_email: str
    user_phone: str
    start_time: str
    end_time: str
    status: str
    created_at: str
    reservation_id: Optional[int] = None


@dataclass
class ConflictingReservationDTO:
    user_name: str
    user_email: str
    user_phone: str
    end_time: str
    start_time: str


@dataclass
class AvailabilityDTO:
    office_id: int
    office_name: str
    is_available: bool
    requested_start_time: str
    requested_end_time: str
    conflicting_reservations: list[ConflictingReservationDTO]
    message: str


@dataclass
class ReservationInfoDTO:
    office_id: int
    office_name: str
    is_occupied: bool
    occupied_by: Optional[str] = None
    occupant_email: Optional[str] = None
    occupant_phone: Optional[str] = None
    until_time: Optional[str] = None
    from_time: Optional[str] = None
    message: str = ""
