from dataclasses import dataclass
from typing import Optional


@dataclass
class Office:
    office_id: int
    name: str
    capacity: int
    description: Optional[str] = None

    def __post_init__(self) -> None:
        self._validate()

    MIN_OFFICE_ID = 1
    MAX_OFFICE_ID = 5

    def _validate(self) -> None:
        if self.office_id < self.MIN_OFFICE_ID or self.office_id > self.MAX_OFFICE_ID:
            raise ValueError(f"Office ID must be between {self.MIN_OFFICE_ID} and {self.MAX_OFFICE_ID}")

        if not self.name or not self.name.strip():
            raise ValueError("Office name cannot be empty")

        if self.capacity < 1:
            raise ValueError("Office capacity must be at least 1")

    def __str__(self) -> str:
        return f"Office {self.office_id}: {self.name} (capacity: {self.capacity})"

    def __repr__(self) -> str:
        return (
            f"Office(office_id={self.office_id}, name='{self.name}', "
            f"capacity={self.capacity}, description='{self.description}')"
        )
