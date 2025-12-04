import sys

from src.bootstrap import get_database_connection, initialize_database, create_dependency_container
from src.presentation.cli.commands import CLI


def main() -> int:
    db = get_database_connection()
    initialize_database(db)
    
    if len(sys.argv) == 1:
        print("Use --help to see available commands")
        return 0
    
    controller, _ = create_dependency_container(db)
    cli = CLI(controller)
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())
