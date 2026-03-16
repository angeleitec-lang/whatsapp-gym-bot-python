import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the application."""
    
    # Flask
    NODE_ENV = os.getenv('NODE_ENV', 'development')
    DEBUG = NODE_ENV == 'development'
    PORT = int(os.getenv('PORT', 3000))
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # WhatsApp Configuration
    WHATSAPP_API_URL = os.getenv('WHATSAPP_API_URL', 'https://graph.instagram.com/v17.0')
    WHATSAPP_PHONE_ID = os.getenv('WHATSAPP_PHONE_ID')
    WHATSAPP_BUSINESS_ACCOUNT_ID = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')
    WHATSAPP_ACCESS_TOKEN = os.getenv('WHATSAPP_ACCESS_TOKEN')
    WEBHOOK_VERIFY_TOKEN = os.getenv('WEBHOOK_VERIFY_TOKEN')
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Google Configuration
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:3000/auth/google/callback')
    GOOGLE_SHEETS_ID = os.getenv('GOOGLE_SHEETS_ID')
    GOOGLE_SHEETS_RANGE = os.getenv('GOOGLE_SHEETS_RANGE', 'scoring!A:I')
    GOOGLE_FORMS_ID = os.getenv('GOOGLE_FORMS_ID')
    GOOGLE_FORMS_URL = os.getenv('GOOGLE_FORMS_URL')
    
    # MySQL Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASS = os.getenv('DB_PASS', '')
    DB_NAME = os.getenv('DB_NAME', 'activate_chat')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    
    # Server Configuration
    TIMEOUT_MESSAGE_MINUTES = int(os.getenv('TIMEOUT_MESSAGE_MINUTES', 1))
    MAX_MESSAGE_LENGTH = 4096

def get_config():
    """Get the appropriate configuration based on the environment."""
    return Config()
