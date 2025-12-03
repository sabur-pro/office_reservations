from abc import ABC, abstractmethod
from dataclasses import dataclass

from ...domain.entities.reservation import Reservation


@dataclass
class NotificationData:
    recipient_name: str
    recipient_email: str
    recipient_phone: str
    office_id: int
    office_name: str
    start_time: str
    end_time: str
    reservation_id: int


class NotificationServiceInterface(ABC):
    @abstractmethod
    def send_email(self, notification_data: NotificationData) -> bool:
        pass
    
    @abstractmethod
    def send_sms(self, notification_data: NotificationData) -> bool:
        pass
    
    def send_all(self, notification_data: NotificationData) -> dict:
        return {
            "email": self.send_email(notification_data),
            "sms": self.send_sms(notification_data)
        }
