from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any


@dataclass(frozen=True)
class TimeSlot:
    start_time: datetime
    end_time: datetime

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if self.start_time >= self.end_time:
            raise ValueError(
                f"Start time ({self.start_time}) must be before end time ({self.end_time})"
            )

        if self.duration() < timedelta(minutes=15):
            raise ValueError("Time slot duration must be at least 15 minutes")

        if self.duration() > timedelta(hours=24):
            raise ValueError("Time slot duration cannot exceed 24 hours")

    def overlaps_with(self, other: "TimeSlot") -> bool:
        return self.start_time < other.end_time and self.end_time > other.start_time

    def is_valid(self) -> bool:
        try:
            self._validate()
            return True
        except ValueError:
            return False

    def duration(self) -> timedelta:
        return self.end_time - self.start_time

    def contains(self, point: datetime) -> bool:
        return self.start_time <= point < self.end_time

    def __str__(self) -> str:
        return f"{self.start_time.strftime('%Y-%m-%d %H:%M')} - {self.end_time.strftime('%H:%M')}"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TimeSlot):
            return False
        return self.start_time == other.start_time and self.end_time == other.end_time

    def __hash__(self) -> int:
        return hash((self.start_time, self.end_time))
