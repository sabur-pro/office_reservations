from datetime import datetime

from ...application.use_cases.check_availability import CheckAvailabilityUseCase
from ...application.use_cases.create_reservation import CreateReservationUseCase
from ...application.use_cases.get_reservation_info import GetReservationInfoUseCase
from ...domain.exceptions.domain_exceptions import (
    OfficeNotFoundError,
    ReservationConflictError,
)
from ...domain.value_objects.time_slot import TimeSlot


class ReservationController:
    def __init__(
        self,
        check_availability_use_case: CheckAvailabilityUseCase,
        create_reservation_use_case: CreateReservationUseCase,
        get_reservation_info_use_case: GetReservationInfoUseCase,
    ) -> None:
        self._check_availability = check_availability_use_case
        self._create_reservation = create_reservation_use_case
        self._get_info = get_reservation_info_use_case

    def check_office_availability(
        self,
        office_id: int,
        date: str,
        start_time: str,
        end_time: str,
    ) -> dict:
        try:
            time_slot = self._parse_time_slot(date, start_time, end_time)
            result = self._check_availability.execute(office_id, time_slot)

            if result.is_available:
                return {
                    "success": True,
                    "available": True,
                    "message": result.message,
                    "data": {
                        "office_id": result.office_id,
                        "office_name": result.office_name,
                    },
                }
            conflicts_info = []
            for conflict in result.conflicting_reservations:
                conflicts_info.append(
                    {
                        "user": conflict.user_name,
                        "email": conflict.user_email,
                        "phone": conflict.user_phone,
                        "until": conflict.end_time,
                    }
                )

            return {
                "success": True,
                "available": False,
                "message": result.message,
                "conflicts": conflicts_info,
            }

        except OfficeNotFoundError:
            return {
                "success": False,
                "error": f"Office {office_id} not found. Please use office ID 1-5.",
            }
        except ValueError as e:
            return {
                "success": False,
                "error": f"Invalid input: {e!s}",
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {e!s}",
            }

    def book_office(  # noqa: PLR0913
        self,
        office_id: int,
        date: str,
        start_time: str,
        end_time: str,
        name: str,
        email: str,
        phone: str,
    ) -> dict:
        try:
            time_slot = self._parse_time_slot(date, start_time, end_time)
            result = self._create_reservation.execute(
                office_id=office_id,
                user_name=name,
                user_email=email,
                user_phone=phone,
                time_slot=time_slot,
            )

            return {
                "success": True,
                "message": (
                    f"[SUCCESS] Successfully booked {result.office_name} "
                    f"(Office #{result.office_id})!\n"
                    f"   Time: {result.start_time} - {result.end_time}\n"
                    f"   Reservation ID: {result.reservation_id}\n"
                    f"   Notifications sent to {result.user_email} and {result.user_phone}"
                ),
                "data": {
                    "reservation_id": result.reservation_id,
                    "office_id": result.office_id,
                    "office_name": result.office_name,
                    "start_time": result.start_time,
                    "end_time": result.end_time,
                },
            }

        except ReservationConflictError as e:
            return {
                "success": False,
                "error": (
                    f"[ERROR] {e.message}\n"
                    f"   Contact: {e.details.get('conflicting_email')}, "
                    f"{e.details.get('conflicting_phone')}"
                ),
            }
        except OfficeNotFoundError:
            return {
                "success": False,
                "error": f"[ERROR] Office {office_id} not found. Please use office ID 1-5.",
            }
        except ValueError as e:
            return {
                "success": False,
                "error": f"[ERROR] Invalid input: {e!s}",
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"[ERROR] Unexpected error: {e!s}",
            }

    def get_office_info(
        self,
        office_id: int,
        date: str,
        start_time: str,
        end_time: str,
    ) -> dict:
        try:
            time_slot = self._parse_time_slot(date, start_time, end_time)
            result = self._get_info.execute(office_id, time_slot)

            if result.is_occupied:
                return {
                    "success": True,
                    "occupied": True,
                    "message": result.message,
                    "data": {
                        "office_id": result.office_id,
                        "office_name": result.office_name,
                        "occupied_by": result.occupied_by,
                        "occupant_email": result.occupant_email,
                        "occupant_phone": result.occupant_phone,
                        "from_time": result.from_time,
                        "until_time": result.until_time,
                    },
                }
            return {
                "success": True,
                "occupied": False,
                "message": result.message,
            }

        except OfficeNotFoundError:
            return {
                "success": False,
                "error": f"Office {office_id} not found. Please use office ID 1-5.",
            }
        except ValueError as e:
            return {
                "success": False,
                "error": f"Invalid input: {e!s}",
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {e!s}",
            }

    @staticmethod
    def _parse_time_slot(date: str, start_time: str, end_time: str) -> TimeSlot:
        try:
            start_datetime = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
            end_datetime = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")

            return TimeSlot(start_time=start_datetime, end_time=end_datetime)

        except ValueError as e:
            raise ValueError(
                f"Invalid date/time format. Use YYYY-MM-DD for date "
                f"and HH:MM for time. Error: {e!s}"
            ) from e
