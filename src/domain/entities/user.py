from dataclasses import dataclass
from typing import Optional

from ..value_objects.contact_info import ContactInfo


@dataclass
class User:
    user_id: Optional[int]
    name: str
    contact_info: ContactInfo

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("User name cannot be empty")

        min_name_length = 2
        if len(self.name.strip()) < min_name_length:
            raise ValueError(f"User name must be at least {min_name_length} characters long")

    def __str__(self) -> str:
        return f"{self.name} ({self.contact_info.email})"

    def __repr__(self) -> str:
        return f"User(user_id={self.user_id}, name='{self.name}', contact_info={self.contact_info})"
