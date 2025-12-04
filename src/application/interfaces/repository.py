from abc import ABC, abstractmethod
from typing import Optional

from ...domain.entities.office import Office
from ...domain.entities.reservation import Reservation
from ...domain.value_objects.time_slot import TimeSlot


class OfficeRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, office_id: int) -> Optional[Office]:
        pass

    @abstractmethod
    def find_all(self) -> list[Office]:
        pass

    @abstractmethod
    def save(self, office: Office) -> Office:
        pass


class ReservationRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, reservation_id: int) -> Optional[Reservation]:
        pass

    @abstractmethod
    def find_all(self) -> list[Reservation]:
        pass

    @abstractmethod
    def find_by_office_and_time(self, office_id: int, time_slot: TimeSlot) -> list[Reservation]:
        pass

    @abstractmethod
    def save(self, reservation: Reservation) -> Reservation:
        pass

    @abstractmethod
    def delete(self, reservation_id: int) -> bool:
        pass
