from config.settings import settings
from src.application.use_cases.check_availability import CheckAvailabilityUseCase
from src.application.use_cases.create_reservation import CreateReservationUseCase
from src.application.use_cases.get_reservation_info import GetReservationInfoUseCase
from src.domain.entities.office import Office
from src.infrastructure.database.connection import DatabaseConnection
from src.infrastructure.database.repositories.office_repository import OfficeRepository
from src.infrastructure.database.repositories.reservation_repository import (
    ReservationRepository,
)
from src.infrastructure.notifications.combined_notifier import (
    CombinedNotificationService,
)
from src.infrastructure.notifications.email_notifier import EmailNotifier
from src.infrastructure.notifications.sms_notifier import SMSNotifier
from src.presentation.controllers.reservation_controller import ReservationController


def initialize_database(db: DatabaseConnection) -> None:
    db.create_tables()

    with db.session_scope() as session:
        office_repo = OfficeRepository(session)

        existing_offices = office_repo.find_all()
        if existing_offices:
            return

        offices = [
            Office(
                office_id=1,
                name="Conference Room A",
                capacity=10,
                description="Large conference room with projector",
            ),
            Office(
                office_id=2,
                name="Meeting Room B",
                capacity=6,
                description="Medium meeting room with whiteboard",
            ),
            Office(
                office_id=3,
                name="Small Meeting Room C",
                capacity=4,
                description="Small room for focused discussions",
            ),
            Office(
                office_id=4,
                name="Executive Suite",
                capacity=8,
                description="Premium meeting space with video conferencing",
            ),
            Office(
                office_id=5,
                name="Collaboration Space",
                capacity=12,
                description="Open collaboration area with multiple zones",
            ),
        ]

        for office in offices:
            office_repo.save(office)


def create_dependency_container(db: DatabaseConnection) -> tuple:
    session = db.get_session()

    office_repository = OfficeRepository(session)
    reservation_repository = ReservationRepository(session)

    email_notifier = EmailNotifier(
        smtp_host=settings.smtp_host,
        smtp_port=settings.smtp_port,
        smtp_username=settings.smtp_username,
        smtp_password=settings.smtp_password,
        from_email=settings.smtp_from_email,
    )
    sms_notifier = SMSNotifier(
        login=settings.osonsms_login,
        hash_key=settings.osonsms_hash,
        sender=settings.osonsms_sender,
        server=settings.osonsms_server,
    )
    notification_service = CombinedNotificationService(
        email_notifier=email_notifier, sms_notifier=sms_notifier
    )

    check_availability_use_case = CheckAvailabilityUseCase(
        office_repository=office_repository, reservation_repository=reservation_repository
    )

    create_reservation_use_case = CreateReservationUseCase(
        office_repository=office_repository,
        reservation_repository=reservation_repository,
        notification_service=notification_service,
    )

    get_reservation_info_use_case = GetReservationInfoUseCase(
        office_repository=office_repository, reservation_repository=reservation_repository
    )

    controller = ReservationController(
        check_availability_use_case=check_availability_use_case,
        create_reservation_use_case=create_reservation_use_case,
        get_reservation_info_use_case=get_reservation_info_use_case,
    )

    return controller, office_repository


def get_database_connection() -> DatabaseConnection:
    return DatabaseConnection(settings.database_url)
