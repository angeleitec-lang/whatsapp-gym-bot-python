"""
Unit tests for WhatsApp service
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from whatsapp_service import WhatsAppService

@pytest.fixture
def mock_config():
    """Create mock configuration."""
    config = Mock()
    config.WHATSAPP_API_URL = "https://graph.instagram.com/v17.0"
    config.WHATSAPP_PHONE_ID = "123456789"
    config.WHATSAPP_ACCESS_TOKEN = "test_token"
    config.WHATSAPP_BUSINESS_ACCOUNT_ID = "987654321"
    return config

@pytest.fixture
def whatsapp_service(mock_config):
    """Create WhatsApp service instance."""
    return WhatsAppService(mock_config)

@patch('whatsapp_service.requests.post')
def test_send_message_success(mock_post, whatsapp_service):
    """Test sending a message successfully."""
    # Mock response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"messages": [{"id": "wamid.123"}]}
    mock_post.return_value = mock_response
    
    # Send message
    result = whatsapp_service.send_message("+34612345678", "Hola")
    
    # Assertions
    assert result["success"] is True
    assert "data" in result
    mock_post.assert_called_once()

@patch('whatsapp_service.requests.post')
def test_send_message_failure(mock_post, whatsapp_service):
    """Test sending a message with API error."""
    # Mock error response
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"
    mock_post.return_value = mock_response
    
    # Send message
    result = whatsapp_service.send_message("+34612345678", "Hola")
    
    # Assertions
    assert result["success"] is False
    assert "error" in result

@patch('whatsapp_service.requests.post')
def test_send_media_message(mock_post, whatsapp_service):
    """Test sending a media message."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"messages": [{"id": "wamid.456"}]}
    mock_post.return_value = mock_response
    
    result = whatsapp_service.send_media_message(
        "+34612345678",
        "https://example.com/image.jpg",
        "image"
    )
    
    assert result["success"] is True

@patch('whatsapp_service.requests.post')
def test_mark_message_read(mock_post, whatsapp_service):
    """Test marking a message as read."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response
    
    result = whatsapp_service.mark_message_read("wamid.123")
    
    assert result["success"] is True

@patch('whatsapp_service.requests.post')
def test_send_message_exception_handling(mock_post, whatsapp_service):
    """Test exception handling in send_message."""
    # Mock exception
    mock_post.side_effect = Exception("Network error")
    
    result = whatsapp_service.send_message("+34612345678", "Hola")
    
    assert result["success"] is False
    assert "error" in result

def test_whatsapp_service_initialization(mock_config):
    """Test WhatsApp service initialization."""
    service = WhatsAppService(mock_config)
    
    assert service.phone_id == "123456789"
    assert service.access_token == "test_token"
    assert service.business_account_id == "987654321"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
