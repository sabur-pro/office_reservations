from ...application.interfaces.notification import (
    NotificationData,
    NotificationServiceInterface,
)
from .email_notifier import EmailNotifier
from .sms_notifier import SMSNotifier


class CombinedNotificationService(NotificationServiceInterface):
    def __init__(
        self,
        email_notifier: EmailNotifier,
        sms_notifier: SMSNotifier
    ) -> None:
        self._email_notifier = email_notifier
        self._sms_notifier = sms_notifier
    
    def send_email(self, notification_data: NotificationData) -> bool:
        return self._email_notifier.send_email(notification_data)
    
    def send_sms(self, notification_data: NotificationData) -> bool:
        return self._sms_notifier.send_sms(notification_data)
