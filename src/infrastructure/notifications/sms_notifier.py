import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Any

from config.logging import get_logger

from ...application.interfaces.notification import (
    NotificationData,
    NotificationServiceInterface,
)

logger = get_logger(__name__)


class SMSNotifier(NotificationServiceInterface):
    def __init__(
        self,
        login: str,
        hash_key: str,
        sender: str,
        server: str,
    ) -> None:
        self._login = login
        self._hash_key = hash_key
        self._sender = sender
        self._server = server

    def send_email(self, _notification_data: NotificationData) -> bool:
        return False

    def send_sms(self, notification_data: NotificationData) -> bool:
        if not self._is_configured():
            logger.warning("SMS not configured, falling back to console mode")
            return self._send_to_console(notification_data)

        try:
            logger.info(f"Sending SMS to {notification_data.recipient_phone}")
            logger.debug(f"OsonSMS Server: {self._server}")
            logger.debug(f"Sender: {self._sender}, Login: {self._login}")

            response = self._send_via_api(notification_data)

            logger.debug(f"OsonSMS Response: {json.dumps(response, ensure_ascii=False)}")

            if response.get("status") == "ok":
                msg_id = response.get("msg_id", "unknown")
                logger.info(f"SMS sent successfully. Message ID: {msg_id}")
                return True

            error_msg = response.get("error", {})
            logger.error(f"OsonSMS error response: {error_msg}")
            return False

        except urllib.error.HTTPError as e:
            logger.error(f"OsonSMS HTTP error {e.code}: {e.reason}")
            try:
                error_body = e.read().decode("utf-8")
                logger.error(f"Response body: {error_body}")
            except Exception:
                pass

        except (urllib.error.URLError, json.JSONDecodeError, OSError) as e:
            logger.error(f"SMS sending error: {type(e).__name__}: {e}")

        return False

    def _is_configured(self) -> bool:
        configured = bool(self._login and self._hash_key and self._sender)
        if not configured:
            logger.debug(
                f"SMS config check - login: {bool(self._login)}, "
                f"hash: {bool(self._hash_key)}, "
                f"sender: {bool(self._sender)}"
            )
        return configured

    def _send_to_console(self, notification_data: NotificationData) -> bool:
        print("=" * 70)
        print("SMS NOTIFICATION (Console Mode)")
        print("=" * 70)
        print(f"To: {notification_data.recipient_phone}")
        print("-" * 70)
        print(self._build_message(notification_data))
        print("=" * 70)
        print()
        return True

    def _send_via_api(self, notification_data: NotificationData) -> dict[str, Any]:
        phone = notification_data.recipient_phone
        message = self._build_message(notification_data)
        txn_id = str(uuid.uuid4())

        str_hash = self._generate_hash(txn_id, phone)

        params = {
            "from": self._sender,
            "phone_number": phone,
            "msg": message,
            "str_hash": str_hash,
            "txn_id": txn_id,
            "login": self._login,
        }

        url = f"{self._server}?{urllib.parse.urlencode(params)}"
        logger.debug(f"Request URL: {self._server}")
        logger.debug(f"Request params (without hash): phone={phone}, txn_id={txn_id}")

        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read().decode("utf-8")
            logger.debug(f"Raw response: {data}")
            result: dict[str, Any] = json.loads(data)
            return result

    def _generate_hash(self, txn_id: str, phone: str) -> str:
        dlm = ";"
        raw = f"{txn_id}{dlm}{self._login}{dlm}{self._sender}{dlm}{phone}{dlm}{self._hash_key}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @staticmethod
    def _build_message(notification_data: NotificationData) -> str:
        return (
            f"Office Reservation Confirmed!\n"
            f"Office: {notification_data.office_name} (#{notification_data.office_id})\n"
            f"Time: {notification_data.start_time} - {notification_data.end_time}\n"
            f"ID: {notification_data.reservation_id}"
        )
