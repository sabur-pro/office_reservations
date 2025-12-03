from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

from .user import User
from ..value_objects.time_slot import TimeSlot


class ReservationStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


@dataclass
class Reservation:
    office_id: int
    user: User
    time_slot: TimeSlot
    reservation_id: Optional[int] = None
    status: ReservationStatus = field(default=ReservationStatus.PENDING)
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self) -> None:
        self._validate()
    
    def _validate(self) -> None:
        if self.office_id < 1 or self.office_id > 5:
            raise ValueError("Office ID must be between 1 and 5")
        
        if not self.time_slot.is_valid():
            raise ValueError("Invalid time slot")
    
    def is_active(self) -> bool:
        return self.status in {
            ReservationStatus.PENDING,
            ReservationStatus.CONFIRMED
        }
    
    def confirm(self) -> None:
        if self.status == ReservationStatus.CANCELLED:
            raise ValueError("Cannot confirm a cancelled reservation")
        
        if self.status == ReservationStatus.COMPLETED:
            raise ValueError("Cannot confirm a completed reservation")
        
        self.status = ReservationStatus.CONFIRMED
    
    def cancel(self) -> None:
        if self.status == ReservationStatus.COMPLETED:
            raise ValueError("Cannot cancel a completed reservation")
        
        if self.status == ReservationStatus.CANCELLED:
            raise ValueError("Reservation is already cancelled")
        
        self.status = ReservationStatus.CANCELLED
    
    def complete(self) -> None:
        if self.status == ReservationStatus.CANCELLED:
            raise ValueError("Cannot complete a cancelled reservation")
        
        self.status = ReservationStatus.COMPLETED
    
    def is_in_past(self) -> bool:
        return self.time_slot.end_time < datetime.now()
    
    def overlaps_with(self, other_time_slot: TimeSlot) -> bool:
        return self.is_active() and self.time_slot.overlaps_with(other_time_slot)
    
    def __str__(self) -> str:
        return (
            f"Reservation #{self.reservation_id}: Office {self.office_id} "
            f"by {self.user.name} ({self.time_slot}) - {self.status.value}"
        )
    
    def __repr__(self) -> str:
        return (
            f"Reservation(reservation_id={self.reservation_id}, "
            f"office_id={self.office_id}, user={self.user}, "
            f"time_slot={self.time_slot}, status={self.status})"
        )
