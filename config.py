import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the application."""
    
    # Default constants
    MAX_MESSAGE_LENGTH = 4096
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        # Flask
        self.NODE_ENV = os.getenv('NODE_ENV', 'development')
        self.DEBUG = self.NODE_ENV == 'development'
        self.PORT = int(os.getenv('PORT', 3000))
        self.SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
        
        # WhatsApp Configuration
        self.WHATSAPP_API_URL = os.getenv('WHATSAPP_API_URL', 'https://graph.instagram.com/v17.0')
        self.WHATSAPP_PHONE_ID = os.getenv('WHATSAPP_PHONE_ID')
        self.WHATSAPP_BUSINESS_ACCOUNT_ID = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')
        self.WHATSAPP_ACCESS_TOKEN = os.getenv('WHATSAPP_ACCESS_TOKEN')
        self.WEBHOOK_VERIFY_TOKEN = os.getenv('WEBHOOK_VERIFY_TOKEN')
        
        # OpenAI Configuration
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        
        # Google Configuration
        self.GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
        self.GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
        self.GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:3000/auth/google/callback')
        self.GOOGLE_SHEETS_ID = os.getenv('GOOGLE_SHEETS_ID')
        self.GOOGLE_SHEETS_RANGE = os.getenv('GOOGLE_SHEETS_RANGE', 'scoring!A:I')
        self.GOOGLE_FORMS_ID = os.getenv('GOOGLE_FORMS_ID')
        self.GOOGLE_FORMS_URL = os.getenv('GOOGLE_FORMS_URL')
        
        # MySQL Configuration
        self.DB_HOST = os.getenv('DB_HOST', 'localhost')
        self.DB_USER = os.getenv('DB_USER', 'root')
        self.DB_PASS = os.getenv('DB_PASS', '')
        self.DB_NAME = os.getenv('DB_NAME', 'activate_chat')
        self.DB_PORT = int(os.getenv('DB_PORT', 3306))
        
        # Server Configuration
        self.TIMEOUT_MESSAGE_MINUTES = int(os.getenv('TIMEOUT_MESSAGE_MINUTES', 1))

def get_config():
    """Get the appropriate configuration based on the environment."""
    return Config()
