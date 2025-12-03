import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ContactInfo:
    email: str
    phone: str
    
    def __post_init__(self) -> None:
        self._validate_email()
        self._validate_phone()
    
    def _validate_email(self) -> None:
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email):
            raise ValueError(f"Invalid email format: {self.email}")
    
    def _validate_phone(self) -> None:
        cleaned_phone = re.sub(r'[\s\-\(\)]', '', self.phone)
        phone_pattern = r'^\+\d{10,15}$'
        if not re.match(phone_pattern, cleaned_phone):
            raise ValueError(
                f"Invalid phone format: {self.phone}. "
                "Must be international format (e.g., +1234567890)"
            )
    
    def __str__(self) -> str:
        return f"{self.email}, {self.phone}"
