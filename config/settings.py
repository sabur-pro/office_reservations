import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv

    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)
except ImportError:
    pass


@dataclass
class Settings:
    database_url: str
    debug: bool

    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    smtp_from_email: str

    osonsms_login: str
    osonsms_hash: str
    osonsms_sender: str
    osonsms_server: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            database_url=os.getenv("DATABASE_URL", ""),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            smtp_host=os.getenv("SMTP_HOST", ""),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            smtp_username=os.getenv("SMTP_USERNAME", ""),
            smtp_password=os.getenv("SMTP_PASSWORD", ""),
            smtp_from_email=os.getenv("SMTP_FROM_EMAIL", ""),
            osonsms_login=os.getenv("OSONSMS_LOGIN", ""),
            osonsms_hash=os.getenv("OSONSMS_HASH", ""),
            osonsms_sender=os.getenv("OSONSMS_SENDER", "OsonSMS"),
            osonsms_server=os.getenv("OSONSMS_SERVER", "https://api.osonsms.com/sendsms_v1.php"),
        )


settings = Settings.from_env()
