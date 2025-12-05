import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config.logging import get_logger

from ...application.interfaces.notification import (
    NotificationData,
    NotificationServiceInterface,
)

logger = get_logger(__name__)


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
            logger.warning("Email not configured, falling back to console mode")
            return self._send_to_console(notification_data)

        try:
            logger.info(f"Sending email to {notification_data.recipient_email}")
            logger.debug(f"SMTP Host: {self._smtp_host}:{self._smtp_port}")
            logger.debug(f"From: {self._from_email}")

            message = self._build_message(notification_data)
            self._send_via_smtp(message, notification_data.recipient_email)

            logger.info(f"Email sent successfully to {notification_data.recipient_email}")
            return True

        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP Authentication failed: {e}")
            logger.error("Check SMTP_USERNAME and SMTP_PASSWORD in .env")
            return False

        except smtplib.SMTPRecipientsRefused as e:
            logger.error(f"Recipient refused: {e}")
            return False

        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {type(e).__name__}: {e}")
            return False

        except OSError as e:
            logger.error(f"Network error: {e}")
            return False

    def send_sms(self, _notification_data: NotificationData) -> bool:
        return False

    def _is_configured(self) -> bool:
        configured = bool(
            self._smtp_host
            and self._smtp_username
            and self._smtp_password
            and self._from_email
        )
        if not configured:
            logger.debug(
                f"Email config check - host: {bool(self._smtp_host)}, "
                f"username: {bool(self._smtp_username)}, "
                f"password: {bool(self._smtp_password)}, "
                f"from_email: {bool(self._from_email)}"
            )
        return configured

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

        logger.debug(f"Connecting to {self._smtp_host}:{self._smtp_port}")

        with smtplib.SMTP(self._smtp_host, self._smtp_port, timeout=30) as server:
            logger.debug("Starting TLS")
            server.starttls(context=context)

            logger.debug(f"Logging in as {self._smtp_username}")
            server.login(self._smtp_username, self._smtp_password)

            logger.debug(f"Sending message to {recipient}")
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
