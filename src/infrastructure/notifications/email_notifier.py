from ...application.interfaces.notification import (
    NotificationData,
    NotificationServiceInterface,
)


class EmailNotifier(NotificationServiceInterface):
    def __init__(self, smtp_host: str = "", smtp_port: int = 587) -> None:
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
    
    def send_email(self, notification_data: NotificationData) -> bool:
        email_content = self._build_email_content(notification_data)
        
        print("=" * 70)
        print("EMAIL NOTIFICATION")
        print("=" * 70)
        print(f"To: {notification_data.recipient_email}")
        print(f"Subject: Office Reservation Confirmation - Office {notification_data.office_id}")
        print("-" * 70)
        print(email_content)
        print("=" * 70)
        print()
        
        return True
    
    def send_sms(self, notification_data: NotificationData) -> bool:
        return False
    
    @staticmethod
    def _build_email_content(notification_data: NotificationData) -> str:
        return f"""
Dear {notification_data.recipient_name},

Your office reservation has been confirmed!

Reservation Details:
--------------------
Office: {notification_data.office_name} (Office #{notification_data.office_id})
Date & Time: {notification_data.start_time} - {notification_data.end_time}
Reservation ID: {notification_data.reservation_id}

Contact Information:
-------------------
Email: {notification_data.recipient_email}
Phone: {notification_data.recipient_phone}

Please arrive on time. If you need to cancel or modify your reservation,
please contact the office administrator.

Best regards,
Office Reservation System
        """.strip()
