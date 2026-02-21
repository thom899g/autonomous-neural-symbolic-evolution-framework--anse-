from typing import Dict, Any, List
import sqlite3

class KnowledgeBase:
    """Manages the knowledge base for the ANSE framework, providing methods to store,
    retrieve, and update facts. It uses SQLite as the underlying storage system.
    
    Attributes:
        db_path (str): Path to the SQLite database file.
        connection: The database connection instance.
        logger (Logger): Logger instance for monitoring KB operations.
    """

    def __init__(self, db_path: str) -> None:
        """Initialize the KnowledgeBase with the specified database path."""
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.logger = logging.getLogger("KnowledgeBase")
        
        # Create table if not exists
        self._initialize_db()

    def _initialize_db(self) -> None:
        """Create the necessary database tables upon initialization."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS facts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject TEXT NOT NULL,
                    predicate TEXT NOT NULL,
                    object TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            self.logger.info("Database initialized successfully.")
        except Exception as e:
            self.logger.error(f"Failed to initialize database: {str(e)}")
            raise

    def store_fact(self, subject: str, predicate: str, object: str) -> int:
        """Store a fact in the knowledge base."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO facts (subject, predicate, object) VALUES (?, ?, ?)",
                (subject, predicate, object)
            )
            self.connection.commit()
            fact_id = cursor.lastrowid
            self.logger.info(f"Fact stored with ID: {fact_id}")
            return fact_id
        except Exception as e:
            self.logger.error(f"Failed to store fact: {str(e)}")
            raise

    def retrieve_fact(self, fact_id: int) -> Dict[str, Any]:
        """Retrieve a fact by its ID."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT * FROM facts WHERE id = ?",
                (fact_id,)
            )
            row = cursor.fetchone()
            if row:
                return {
                    "id": row[0],
                    "subject": row[1],
                    "predicate": row[2],
                    "object": row[3],
                    "timestamp": row[4]
                }
            else:
                raise ValueError(f"Fact with ID {fact_id} not found.")
        except Exception as e:
            self.logger.error(f"Failed to retrieve fact: {str(e)}")
            raise

    def update_fact(self, fact_id: int, new_object: str) ->