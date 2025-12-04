import os
from dataclasses import dataclass


@dataclass
class Settings:
    database_url: str = "postgresql://office_user:123456@localhost:5432/office_reservations"

    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""

    sms_api_key: str = ""
    sms_sender_number: str = ""

    debug: bool = False

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            database_url=os.getenv(
                "DATABASE_URL", "postgresql://office_user:123456@localhost:5432/office_reservations"
            ),
            smtp_host=os.getenv("SMTP_HOST", ""),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            smtp_username=os.getenv("SMTP_USERNAME", ""),
            smtp_password=os.getenv("SMTP_PASSWORD", ""),
            sms_api_key=os.getenv("SMS_API_KEY", ""),
            sms_sender_number=os.getenv("SMS_SENDER_NUMBER", ""),
            debug=os.getenv("DEBUG", "false").lower() == "true",
        )


settings = Settings.from_env()
