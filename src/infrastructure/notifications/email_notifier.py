import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ...application.interfaces.notification import (
    NotificationData,
    NotificationServiceInterface,
)


class EmailNotifier(NotificationServiceInterface):
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_username: str,
        smtp_password: str,
        from_email: str,
    ) -> None:
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._smtp_username = smtp_username
        self._smtp_password = smtp_password
        self._from_email = from_email

    def send_email(self, notification_data: NotificationData) -> bool:
        if not self._is_configured():
            return self._send_to_console(notification_data)

        try:
            message = self._build_message(notification_data)
            self._send_via_smtp(message, notification_data.recipient_email)
            return True
        except (smtplib.SMTPException, OSError):
            return False

    def send_sms(self, _notification_data: NotificationData) -> bool:
        return False

    def _is_configured(self) -> bool:
        return bool(
            self._smtp_host
            and self._smtp_username
            and self._smtp_password
            and self._from_email
        )

    def _send_to_console(self, notification_data: NotificationData) -> bool:
        print("=" * 70)
        print("EMAIL NOTIFICATION (Console Mode)")
        print("=" * 70)
        print(f"To: {notification_data.recipient_email}")
        print(f"Subject: Office Reservation - Office {notification_data.office_id}")
        print("-" * 70)
        print(self._build_body(notification_data))
        print("=" * 70)
        print()
        return True

    def _build_message(self, notification_data: NotificationData) -> MIMEMultipart:
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Office Reservation - Office {notification_data.office_id}"
        message["From"] = self._from_email
        message["To"] = notification_data.recipient_email

        body = self._build_body(notification_data)
        message.attach(MIMEText(body, "plain", "utf-8"))

        return message

    def _send_via_smtp(self, message: MIMEMultipart, recipient: str) -> None:
        context = ssl.create_default_context()

        with smtplib.SMTP(self._smtp_host, self._smtp_port) as server:
            server.starttls(context=context)
            server.login(self._smtp_username, self._smtp_password)
            server.sendmail(self._from_email, recipient, message.as_string())

    @staticmethod
    def _build_body(notification_data: NotificationData) -> str:
        return f"""Dear {notification_data.recipient_name},

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
Office Reservation System"""
