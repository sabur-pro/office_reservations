
import argparse
from typing import Optional

from ..controllers.reservation_controller import ReservationController


class CLI:
    def __init__(self, controller: ReservationController) -> None:
        self._controller = controller
        self._parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Office Reservation System",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python main.py check-availability --office-id 1 --date 2025-12-03 --start-time 10:00 --end-time 12:00
  python main.py book --office-id 1 --date 2025-12-03 --start-time 10:00 --end-time 12:00 \\
      --name "Farrukh Rahimov" --email "farrukh@example.tj" --phone "+992901234567"
  python main.py info --office-id 1 --date 2025-12-03 --start-time 10:00 --end-time 12:00
            """,
        )

        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        check_parser = subparsers.add_parser(
            "check-availability", help="Check if an office is available"
        )
        self._add_common_args(check_parser)

        book_parser = subparsers.add_parser("book", help="Book an office")
        self._add_common_args(book_parser)
        book_parser.add_argument("--name", required=True, help="Your name")
        book_parser.add_argument("--email", required=True, help="Your email address")
        book_parser.add_argument(
            "--phone",
            required=True,
            help="Your phone number (international format, e.g., +1234567890)",
        )

        info_parser = subparsers.add_parser("info", help="Get information about office occupancy")
        self._add_common_args(info_parser)

        return parser

    @staticmethod
    def _add_common_args(parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--office-id", type=int, required=True, choices=[1, 2, 3, 4, 5], help="Office ID (1-5)"
        )
        parser.add_argument("--date", required=True, help="Date (YYYY-MM-DD)")
        parser.add_argument("--start-time", required=True, help="Start time (HH:MM)")
        parser.add_argument("--end-time", required=True, help="End time (HH:MM)")

    def run(self, args: Optional[list[str]] = None) -> int:
        parsed_args = self._parser.parse_args(args)

        if not parsed_args.command:
            self._parser.print_help()
            return 1

        if parsed_args.command == "check-availability":
            return self._handle_check_availability(parsed_args)
        if parsed_args.command == "book":
            return self._handle_book(parsed_args)
        if parsed_args.command == "info":
            return self._handle_info(parsed_args)
        print(f"Unknown command: {parsed_args.command}")
        return 1

    def _handle_check_availability(self, args: argparse.Namespace) -> int:
        result = self._controller.check_office_availability(
            office_id=args.office_id,
            date=args.date,
            start_time=args.start_time,
            end_time=args.end_time,
        )

        if not result["success"]:
            print(f"Error: {result['error']}")
            return 1

        print("\n" + "=" * 70)
        print("OFFICE AVAILABILITY CHECK")
        print("=" * 70)

        if result["available"]:
            print(f"[OK] {result['message']}")
        else:
            print(f"[NOT AVAILABLE] {result['message']}\n")
            print("Conflicting reservations:")
            for i, conflict in enumerate(result.get("conflicts", []), 1):
                print(f"  {i}. {conflict['user']}")
                print(f"     Email: {conflict['email']}")
                print(f"     Phone: {conflict['phone']}")
                print(f"     Until: {conflict['until']}")
                print()

        print("=" * 70 + "\n")
        return 0

    def _handle_book(self, args: argparse.Namespace) -> int:
        result = self._controller.book_office(
            office_id=args.office_id,
            date=args.date,
            start_time=args.start_time,
            end_time=args.end_time,
            name=args.name,
            email=args.email,
            phone=args.phone,
        )

        if not result["success"]:
            print(f"\n{result['error']}\n")
            return 1

        print("\n" + "=" * 70)
        print("RESERVATION CONFIRMATION")
        print("=" * 70)
        print(result["message"])
        print("=" * 70 + "\n")
        return 0

    def _handle_info(self, args: argparse.Namespace) -> int:
        result = self._controller.get_office_info(
            office_id=args.office_id,
            date=args.date,
            start_time=args.start_time,
            end_time=args.end_time,
        )

        if not result["success"]:
            print(f"Error: {result['error']}")
            return 1

        print("\n" + "=" * 70)
        print("OFFICE INFORMATION")
        print("=" * 70)

        if result["occupied"]:
            print("[OCCUPIED] Office is OCCUPIED\n")
            print(f"Office: {result['data']['office_name']} (#{result['data']['office_id']})")
            print(f"Occupied by: {result['data']['occupied_by']}")
            print(
                f"Contact: {result['data']['occupant_email']}, {result['data']['occupant_phone']}"
            )
            print(f"From: {result['data']['from_time']}")
            print(f"Until: {result['data']['until_time']}")
        else:
            print(f"[FREE] {result['message']}")

        print("=" * 70 + "\n")
        return 0
