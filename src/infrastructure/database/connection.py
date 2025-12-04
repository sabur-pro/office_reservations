from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

Base = declarative_base()


class DatabaseConnection:
    def __init__(self, database_url: str) -> None:
        self._engine = create_engine(database_url, echo=False)
        self._session_factory = sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
        )

    def create_tables(self) -> None:
        Base.metadata.create_all(bind=self._engine)

    def drop_tables(self) -> None:
        Base.metadata.drop_all(bind=self._engine)

    def get_session(self) -> Session:
        return self._session_factory()

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
