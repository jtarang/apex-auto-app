import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class DatabaseManager:
    """
    Manages the database connection, engine, session factory
    """

    def __init__(self):
        """
        Initializes the manager, loads necessary environment variables,
        and sets up the connection arguments.
        """
        self.database_url = os.environ.get("DATABASE_URL")
        self.cert_ca = os.environ.get("DB_CERT_CA_PATH")
        self.cert_client = os.environ.get("DB_CLIENT_CERT_PATH")
        self.key_client = os.environ.get("DB_CLIENT_KEY_PATH")

        self.engine = None
        self.session_local = None
        self._sync_connect_args = None

        self._validate_config()
        self._setup_connect_args()
        self.setup_engine_and_session()

    def _validate_config(self):
        """Checks for required environment variables."""
        if not all([self.database_url, self.cert_ca, self.cert_client, self.key_client]):
            raise ValueError(
                "Missing one or more database connection environment variables "
                "(DATABASE_URL, DB_CERT_CA_PATH, DB_CLIENT_CERT_PATH, DB_CLIENT_KEY_PATH)."
            )

    def _setup_connect_args(self):
        """
        Creates the connection arguments for SQLAlchemy using SSL/TLS files.
        """
        try:
            self._sync_connect_args = {
                'sslmode': 'verify-full',
                'sslrootcert': self.cert_ca,
                'sslcert': self.cert_client,
                'sslkey': self.key_client
            }
        except FileNotFoundError as e:
            print(f"ERROR: Certificate file not found: {e}")
            raise

    def setup_engine_and_session(self):
        """
        Creates the SQLAlchemy Engine and the Synchronous Session Factory.
        """
        if not self._sync_connect_args:
            raise RuntimeError("Connection arguments not initialized. Cannot set up engine.")

        self.engine = create_engine(
            self.database_url,
            echo=True,  # Logs SQL queries
            connect_args=self._sync_connect_args
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