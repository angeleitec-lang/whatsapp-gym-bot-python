"""
Unit tests for configuration module
"""
from unittest.mock import patch

import pytest

from config import Config, get_config


def test_config_default_values():
    """Test default configuration values."""
    config = Config()
    
    assert config.NODE_ENV == 'development'
    assert config.PORT == 3000
    assert config.TIMEOUT_MESSAGE_MINUTES == 1

@patch.dict('os.environ', {
    'NODE_ENV': 'production',
    'PORT': '8000',
    'WHATSAPP_PHONE_ID': 'test_phone_id',
    'WHATSAPP_ACCESS_TOKEN': 'test_token'
})
def test_config_from_env():
    """Test configuration from environment variables."""
    config = Config()
    
    assert config.NODE_ENV == 'production'
    assert config.PORT == 8000
    assert config.WHATSAPP_PHONE_ID == 'test_phone_id'
    assert config.WHATSAPP_ACCESS_TOKEN == 'test_token'

def test_config_debug_mode():
    """Test debug mode based on environment."""
    config = Config()
    assert config.DEBUG == (config.NODE_ENV == 'development')

def test_get_config_singleton():
    """Test get_config returns Config instance."""
    config = get_config()
    assert isinstance(config, Config)

@patch.dict('os.environ', {
    'DB_HOST': 'localhost',
    'DB_USER': 'root',
    'DB_PASS': 'password',
    'DB_NAME': 'test_db',
    'DB_PORT': '3307'
})
def test_database_config():
    """Test database configuration."""
    config = Config()
    
    assert config.DB_HOST == 'localhost'
    assert config.DB_USER == 'root'
    assert config.DB_PASS == 'password'
    assert config.DB_NAME == 'test_db'
    assert config.DB_PORT == 3307

@patch.dict('os.environ', {
    'GOOGLE_CLIENT_ID': 'test_client_id',
    'GOOGLE_CLIENT_SECRET': 'test_secret',
    'GOOGLE_SHEETS_ID': 'test_sheet_id'
})
def test_google_config():
    """Test Google configuration."""
    config = Config()
    
    assert config.GOOGLE_CLIENT_ID == 'test_client_id'
    assert config.GOOGLE_CLIENT_SECRET == 'test_secret'
    assert config.GOOGLE_SHEETS_ID == 'test_sheet_id'

@patch.dict('os.environ', {'OPENAI_API_KEY': 'test_openai_key'})
def test_openai_config():
    """Test OpenAI configuration."""
    config = Config()
    assert config.OPENAI_API_KEY == 'test_openai_key'

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
