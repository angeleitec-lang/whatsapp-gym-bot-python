"""
Database Service for MySQL operations
"""
from datetime import datetime

import mysql.connector
from mysql.connector import Error

from config import Config
from logger import get_logger

logger = get_logger(__name__)

class DatabaseService:
    """Service for MySQL database operations."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.connection = None
        self.connect()
    
    def connect(self):
        """Establish a connection to the database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.config.DB_HOST,
                user=self.config.DB_USER,
                password=self.config.DB_PASS,
                database=self.config.DB_NAME,
                port=self.config.DB_PORT
            )
            logger.info("Database connection established successfully")
        except Error as e:
            logger.error(f"Error connecting to database: {str(e)}")
            self.connection = None
    
    def is_connected(self) -> bool:
        """Check if database is connected."""
        if self.connection is None:
            return False
        
        try:
            self.connection.ping()
            return True
        except Error:
            return False
    
    def log_message(self, phone_number: str, sender: str, message: str, 
                   message_type: str = "text") -> bool:
        """
        Log a message to the database.
        
        Args:
            phone_number: Client phone number
            sender: Who sent the message (user, bot)
            message: Message content
            message_type: Type of message (text, image, video, etc.)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.is_connected():
                self.connect()
            
            cursor = self.connection.cursor()
            
            query = """
            INSERT INTO messages 
            (phone_number, sender, message_content, message_type, created_at) 
            VALUES (%s, %s, %s, %s, %s)
            """
            
            values = (phone_number, sender, message, message_type, datetime.now())
            
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            
            logger.info(f"Message logged for {phone_number}")
            return True
            
        except Error as e:
            logger.error(f"Error logging message: {str(e)}")
            return False
    
    def log_client_score(self, phone_number: str, client_name: str, age: int,
                         experience: str, problems: str, perception: str,
                         objectives: str, days_per_week: int, format_type: str,
                         availability: str, score: int, category: str, email_sent: bool = False) -> bool:
        """
        Log a client scoring record.
        
        Args:
            phone_number: Client phone number
            client_name: Client name
            age: Client age
            experience: Previous training experience
            problems: Physical problems/limitations
            perception: Physical perception
            objectives: Training objectives
            days_per_week: Desired training days per week
            format_type: Training format preference
            availability: Time availability
            score: Client score (0-100)
            category: Client category (Frío, Tibio, Caliente)
            email_sent: Whether email was sent
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.is_connected():
                self.connect()
            
            cursor = self.connection.cursor()
            
            query = """
            INSERT INTO clients_scoring 
            (phone_number, client_name, age, previous_experience, physical_problems, 
             physical_perception, objectives, days_per_week, training_format, 
             time_availability, score, category, email_sent, created_at) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (phone_number, client_name, age, experience, problems, perception,
                     objectives, days_per_week, format_type, availability, score, 
                     category, email_sent, datetime.now())
            
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            
            logger.info(f"Client score logged for {client_name} ({phone_number})")
            return True
            
        except Error as e:
            logger.error(f"Error logging client score: {str(e)}")
            return False
    
    def create_chat_session(self, phone_number: str, client_name: str = None) -> str:
        """
        Create a new chat session.
        
        Args:
            phone_number: Client phone number
            client_name: Optional client name
            
        Returns:
            Session ID if successful, None otherwise
        """
        try:
            if not self.is_connected():
                self.connect()
            
            cursor = self.connection.cursor()
            
            query = """
            INSERT INTO chat_sessions 
            (phone_number, client_name, started_at, last_activity) 
            VALUES (%s, %s, %s, %s)
            """
            
            now = datetime.now()
            values = (phone_number, client_name, now, now)
            
            cursor.execute(query, values)
            self.connection.commit()
            
            session_id = cursor.lastrowid
            cursor.close()
            
            logger.info(f"Chat session created: {session_id}")
            return str(session_id)
            
        except Error as e:
            logger.error(f"Error creating chat session: {str(e)}")
            return None
    
    def update_session_activity(self, session_id: str) -> bool:
        """Update the last activity timestamp for a session."""
        try:
            if not self.is_connected():
                self.connect()
            
            cursor = self.connection.cursor()
            
            query = """
            UPDATE chat_sessions 
            SET last_activity = %s 
            WHERE id = %s
            """
            
            cursor.execute(query, (datetime.now(), session_id))
            self.connection.commit()
            cursor.close()
            
            return True
            
        except Error as e:
            logger.error(f"Error updating session activity: {str(e)}")
            return False
    
    def get_client_history(self, phone_number: str, limit: int = 50) -> list:
        """
        Get message history for a client.
        
        Args:
            phone_number: Client phone number
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of message records
        """
        try:
            if not self.is_connected():
                self.connect()
            
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
            SELECT * FROM messages 
            WHERE phone_number = %s 
            ORDER BY created_at DESC 
            LIMIT %s
            """
            
            cursor.execute(query, (phone_number, limit))
            results = cursor.fetchall()
            cursor.close()
            
            return results
            
        except Error as e:
            logger.error(f"Error retrieving client history: {str(e)}")
            return []
    
    def close(self):
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Database connection closed")

# Create singleton instance
_db_service = None

def get_database_service():
    """Get or create database service singleton."""
    global _db_service
    if _db_service is None:
        _db_service = DatabaseService()
    return _db_service
