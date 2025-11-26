from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


class DatabaseManager:
    """
    Manages the database connection, engine, session factory
    """

    def __init__(self):
        """
        Initializes the manager, loads necessary environment variables,
        and sets up the connection arguments.
        """
        self.database_url = environ.get("DATABASE_URI")

        self.engine = None
        self.session_local = None
        self._sync_connect_args = None

        self.setup_engine_and_session()

    def setup_engine_and_session(self):
        """
        Creates the SQLAlchemy Engine and the Synchronous Session Factory.
        """
        if not self.database_url:
            raise RuntimeError("Connection arguments not initialized. Cannot set up engine.")

        self.engine = create_engine(
            self.database_url,
            echo=True,  # Logs SQL queries
        )

        self.session_local = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )

    def get_db_session(self):
        """
        FastAPI dependency: provides a synchronous database session.
        Ensures the session is closed after use, even if errors occur.
        """
        if not self.session_local:
            raise RuntimeError("SessionLocal factory not initialized.")

        session: Session = self.session_local()
        try:
            return session
        finally:
            session.close()