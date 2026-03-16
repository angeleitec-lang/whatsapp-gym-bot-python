"""
Integration tests for Flask application
"""
import json
from unittest.mock import Mock, patch

import pytest

from app import app


@pytest.fixture
def client():
    """Create Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test health check endpoint."""
    response = client.get('/health')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'ok'
    assert 'message' in data

def test_webhook_verify_invalid_token(client):
    """Test webhook verification with invalid token."""
    response = client.get('/webhook?hub.mode=subscribe&hub.challenge=test&hub.verify_token=invalid')
    
    assert response.status_code == 403

@patch('app.config.WEBHOOK_VERIFY_TOKEN', 'test_token')
def test_webhook_verify_valid_token(client):
    """Test webhook verification with valid token."""
    response = client.get('/webhook?hub.mode=subscribe&hub.challenge=test_challenge&hub.verify_token=test_token')
    
    assert response.status_code == 200
    assert response.data == b'test_challenge'

@patch('app.orchestrator.handle_message')
def test_webhook_message_handler(mock_handle, client):
    """Test webhook message handler."""
    mock_handle.return_value = {'success': True}
    
    payload = {
        'object': 'whatsapp_business_account',
        'entry': [{
            'changes': [{
                'value': {
                    'messages': [{
                        'from': '+34612345678',
                        'id': 'wamid.123',
                        'text': {'body': 'Hola'}
                    }]
                }
            }]
        }]
    }
    
    response = client.post('/webhook', 
                          json=payload,
                          content_type='application/json')
    
    assert response.status_code == 200
    mock_handle.assert_called_once()

def test_not_found_endpoint(client):
    """Test 404 error handler."""
    response = client.get('/nonexistent')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data

@patch('app.orchestrator.whatsapp_service.send_message')
def test_test_send_message_endpoint(mock_send, client):
    """Test /test/send-message endpoint."""
    mock_send.return_value = {'success': True}
    
    payload = {
        'phone_number': '+34612345678',
        'message': 'Test message'
    }
    
    response = client.post('/test/send-message',
                          json=payload,
                          content_type='application/json')
    
    assert response.status_code == 200
    mock_send.assert_called_once()

def test_test_send_message_missing_fields(client):
    """Test /test/send-message with missing fields."""
    payload = {'phone_number': '+34612345678'}
    
    response = client.post('/test/send-message',
                          json=payload,
                          content_type='application/json')
    
    assert response.status_code == 400

@patch('app.orchestrator.sheets_service.append_row')
def test_test_sheets_endpoint(mock_append, client):
    """Test /test/sheets endpoint."""
    mock_append.return_value = True
    
    payload = {
        'nome': 'Juan',
        'edad': 50,
        'score': 75,
        'categoria': 'Caliente'
    }
    
    response = client.post('/test/sheets',
                          json=payload,
                          content_type='application/json')
    
    assert response.status_code == 200
    mock_append.assert_called_once()

def test_test_qa_endpoint(client):
    """Test /test/qa endpoint."""
    payload = {'question': '¿Es seguro entrenar a los 50 años?'}
    
    response = client.post('/test/qa',
                          json=payload,
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'question' in data
    assert 'matches_found' in data
    assert 'results' in data

def test_test_qa_no_matches(client):
    """Test /test/qa with no matching questions."""
    payload = {'question': 'xyzabc123nonsense'}
    
    response = client.post('/test/qa',
                          json=payload,
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['matches_found'] == 0

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
