import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Any

from ...application.interfaces.notification import (
    NotificationData,
    NotificationServiceInterface,
)


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
            return self._send_to_console(notification_data)

        try:
            response = self._send_via_api(notification_data)
            return response.get("status") == "ok"
        except (urllib.error.URLError, json.JSONDecodeError, OSError):
            return False

    def _is_configured(self) -> bool:
        return bool(self._login and self._hash_key and self._sender)

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

        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read().decode("utf-8")
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
