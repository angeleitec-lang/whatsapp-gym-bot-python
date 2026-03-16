"""
Flask application for WhatsApp Chatbot
Main entry point for the application
"""
import hashlib
import hmac

from flask import Flask, jsonify, request
from flask_cors import CORS

from chatbot_orchestrator import get_chatbot_orchestrator
from config import Config
from logger import get_logger

app = Flask(__name__)
CORS(app)

config = Config()
logger = get_logger(__name__)
orchestrator = get_chatbot_orchestrator()

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "message": "WhatsApp Gym Chatbot is running",
        "environment": config.NODE_ENV
    }), 200

# WhatsApp Webhook verification
@app.route('/webhook', methods=['GET'])
def webhook_verify():
    """
    Webhook verification endpoint for WhatsApp.
    Meta sends a GET request to verify the webhook.
    """
    try:
        mode = request.args.get('hub.mode')
        challenge = request.args.get('hub.challenge')
        verify_token = request.args.get('hub.verify_token')
        
        # Verify the token
        if mode == 'subscribe' and verify_token == config.WEBHOOK_VERIFY_TOKEN:
            logger.info("Webhook verified successfully")
            return challenge, 200
        else:
            logger.warning("Webhook verification failed - invalid token")
            return 'Forbidden', 403
            
    except Exception as e:
        logger.error(f"Error verifying webhook: {str(e)}")
        return 'Error', 500

# WhatsApp Message handler
@app.route('/webhook', methods=['POST'])
def webhook_handle():
    """
    Handle incoming WhatsApp messages.
    """
    try:
        data = request.get_json()
        
        # Log incoming webhook
        logger.debug(f"Webhook received: {data}")
        
        # Check if this is a message webhook
        if data.get('object') == 'whatsapp_business_account':
            entry = data.get('entry', [])[0]
            changes = entry.get('changes', [])[0]
            value = changes.get('value', {})
            
            # Check for messages
            messages = value.get('messages', [])
            if messages:
                for message in messages:
                    result = orchestrator.handle_message(message)
                    if not result['success']:
                        logger.error(f"Failed to handle message: {result.get('error')}")
            
            # Check for status updates
            statuses = value.get('statuses', [])
            if statuses:
                for status in statuses:
                    logger.info(f"Message status update: {status}")
        
        # Always return 200 to acknowledge receipt
        return jsonify({"status": "received"}), 200
        
    except Exception as e:
        logger.error(f"Error handling webhook: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Google Forms submission handler
@app.route('/form-submission', methods=['POST'])
def form_submission():
    """
    Handle Google Forms submissions via Apps Script webhook.
    """
    try:
        data = request.get_json()
        
        logger.info(f"Form submission received from Apps Script")
        
        # Add phone number if not present
        phone_number = data.get('from', '')
        if not phone_number:
            # Try to extract from context
            phone_number = data.get('clientData', {}).get('phone', '')
        
        # Handle form submission
        result = orchestrator._handle_form_submission({
            **data,
            'from': phone_number
        })
        
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        logger.error(f"Error handling form submission: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Test endpoint for development
@app.route('/test/send-message', methods=['POST'])
def test_send_message():
    """Test endpoint to send a message."""
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')
        message = data.get('message')
        
        if not phone_number or not message:
            return jsonify({"error": "Missing phone_number or message"}), 400
        
        # Ensure phone number is in E.164 format
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
        
        result = orchestrator.whatsapp_service.send_message(phone_number, message)
        return jsonify(result), 200 if result['success'] else 400
        
    except Exception as e:
        logger.error(f"Error in test endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Test endpoint for sheets
@app.route('/test/sheets', methods=['POST'])
def test_sheets():
    """Test endpoint for Google Sheets integration."""
    try:
        data = request.get_json()
        
        # Append test data to sheets
        row_values = [
            data.get('nombre', 'Test'),
            data.get('edad', 50),
            data.get('experiencia', ''),
            data.get('problemas', ''),
            data.get('percepcion', ''),
            data.get('objetivos', ''),
            data.get('dias', 2),
            data.get('formato', 'Grupo'),
            data.get('disponibilidad', 'Mañanas'),
            data.get('score', 50),
            data.get('categoria', 'Tibio'),
            'No'
        ]
        
        result = orchestrator.sheets_service.append_row(row_values)
        return jsonify({
            "success": result,
            "message": "Test data added to sheets"
        }), 200 if result else 400
        
    except Exception as e:
        logger.error(f"Error in sheets test: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Test Q&A endpoint
@app.route('/test/qa', methods=['POST'])
def test_qa():
    """Test the Q&A system."""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        from qa_database import search_qa
        results = search_qa(question)
        
        return jsonify({
            "question": question,
            "matches_found": len(results),
            "results": results[:3]  # Return top 3 matches
        }), 200
        
    except Exception as e:
        logger.error(f"Error in QA test: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    logger.info(f"Starting WhatsApp Gym Chatbot in {config.NODE_ENV} mode")
    app.run(
        host='0.0.0.0',
        port=config.PORT,
        debug=config.DEBUG
    )
