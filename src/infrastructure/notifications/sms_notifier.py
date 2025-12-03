from ...application.interfaces.notification import (
    NotificationData,
    NotificationServiceInterface,
)


class SMSNotifier(NotificationServiceInterface):
    def __init__(self, api_key: str = "", sender_number: str = "") -> None:
        self._api_key = api_key
        self._sender_number = sender_number
    
    def send_email(self, notification_data: NotificationData) -> bool:
        return False
    
    def send_sms(self, notification_data: NotificationData) -> bool:
        sms_content = self._build_sms_content(notification_data)
        
        print("=" * 70)
        print("SMS NOTIFICATION")
        print("=" * 70)
        print(f"To: {notification_data.recipient_phone}")
        print("-" * 70)
        print(sms_content)
        print("=" * 70)
        print()
        
        return True
    
    @staticmethod
    def _build_sms_content(notification_data: NotificationData) -> str:
        return (
            f"Office Reservation Confirmed!\n"
            f"Office: {notification_data.office_name} (#{notification_data.office_id})\n"
            f"Time: {notification_data.start_time} - {notification_data.end_time}\n"
            f"ID: {notification_data.reservation_id}"
        )
