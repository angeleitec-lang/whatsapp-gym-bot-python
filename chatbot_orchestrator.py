"""
Chatbot Orchestrator - Main logic for handling messages
"""
import threading
import time
from datetime import datetime, timedelta
from qa_database import search_qa, get_qa_database
from whatsapp_service import get_whatsapp_service
from chatgpt_service import get_chatgpt_service
from database_service import get_database_service
from google_sheets_service import get_sheets_service
from logger import get_logger

logger = get_logger(__name__)

class ChatbotOrchestrator:
    """Main orchestrator for chatbot logic."""
    
    def __init__(self):
        self.whatsapp_service = get_whatsapp_service()
        self.chatgpt_service = get_chatgpt_service()
        self.database_service = get_database_service()
        self.sheets_service = get_sheets_service()
        
        # Track inactivity timeouts per user
        self.user_timeouts = {}
        self.start_timeout_monitor()
    
    def handle_message(self, message_data: dict) -> dict:
        """
        Main handler for incoming WhatsApp messages.
        
        Args:
            message_data: Dictionary with message information
            
        Returns:
            Response result
        """
        try:
            phone_number = message_data.get('from')
            message_text = message_data.get('text', {}).get('body', '')
            message_id = message_data.get('id')
            
            # Mark message as read
            if message_id:
                self.whatsapp_service.mark_message_read(message_id)
            
            # Log incoming message
            self.database_service.log_message(phone_number, 'user', message_text)
            
            # Check if it's a form submission
            if self._is_form_submission(message_data):
                return self._handle_form_submission(message_data)
            
            # Get response
            response = self._get_response(phone_number, message_text)
            
            # Send response back
            result = self.whatsapp_service.send_message(phone_number, response)
            
            # Log response
            if result['success']:
                self.database_service.log_message(phone_number, 'bot', response)
                self._reset_timeout(phone_number)
            
            return result
            
        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _get_response(self, phone_number: str, message: str) -> str:
        """
        Get response for a user message.
        Tries Q&A first, then falls back to ChatGPT.
        """
        try:
            # Search Q&A database
            qa_results = search_qa(message)
            
            if qa_results:
                logger.info(f"Found {len(qa_results)} Q&A matches")
                # Use the best match
                return qa_results[0]['answer']
            
            # Fall back to ChatGPT
            logger.info("No Q&A match, using ChatGPT")
            result = self.chatgpt_service.get_response(message)
            
            if result['success']:
                return result['response']
            else:
                return "Lo siento, no pude procesar tu pregunta. Por favor, intenta de nuevo."
                
        except Exception as e:
            logger.error(f"Error getting response: {str(e)}")
            return "Disculpa, hubo un error. Por favor, intenta de nuevo."
    
    def _is_form_submission(self, message_data: dict) -> bool:
        """Check if this is a form submission."""
        return 'form_submission' in message_data
    
    def _handle_form_submission(self, form_data: dict) -> dict:
        """Handle form submission data."""
        try:
            client_data = form_data.get('clientData', {})
            phone_number = form_data.get('from')
            
            # Extract data
            client_name = client_data.get('nombre', 'Unknown')
            age = int(client_data.get('edad', 0)) if client_data.get('edad') else 0
            experience = client_data.get('experienciaPrevia', '')
            problems = client_data.get('problemasLimitaciones', '')
            perception = client_data.get('percepcionFisica', '')
            objectives = client_data.get('objetivos', '')
            days_per_week = int(client_data.get('diasPorSemana', 0)) if client_data.get('diasPorSemana') else 0
            format_type = client_data.get('formatoEntrenamiento', '')
            availability = client_data.get('disponibilidadHoraria', '')
            
            # Score the client
            scoring_result = self.chatgpt_service.score_client(client_data)
            
            if scoring_result['success']:
                score_data = scoring_result['data']
                score = score_data.get('score', 0)
                category = score_data.get('category', 'Tibio')
                
                # Log to database
                self.database_service.log_client_score(
                    phone_number=phone_number,
                    client_name=client_name,
                    age=age,
                    experience=experience,
                    problems=problems,
                    perception=perception,
                    objectives=objectives,
                    days_per_week=days_per_week,
                    format_type=format_type,
                    availability=availability,
                    score=score,
                    category=category
                )
                
                # Update Google Sheets
                self._update_sheets_with_client(
                    client_name, age, experience, problems, perception,
                    objectives, days_per_week, format_type, availability, score, category
                )
                
                # Generate and send email
                self._send_personalized_email(client_data, score, category)
                
                # Send WhatsApp confirmation
                confirmation_msg = f"¡Gracias {client_name}! Hemos recibido tu información y te contactaremos pronto. Tu puntuación: {score}/100"
                self.whatsapp_service.send_message(phone_number, confirmation_msg)
                
                logger.info(f"Form submission processed for {client_name}")
                return {"success": True, "client_score": score, "category": category}
            
            return {"success": False, "error": "Could not score client"}
            
        except Exception as e:
            logger.error(f"Error handling form submission: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _update_sheets_with_client(self, name, age, experience, problems, perception,
                                   objectives, days_per_week, format_type, availability, score, category):
        """Update Google Sheets with client information."""
        try:
            row_values = [
                datetime.now().strftime('%Y-%m-%d'),
                name,
                str(age),
                experience,
                problems,
                perception,
                objectives,
                str(days_per_week),
                format_type,
                availability,
                str(score),
                category,
                'No'
            ]
            
            self.sheets_service.append_row(row_values)
            logger.info(f"Client data added to Google Sheets: {name}")
            
        except Exception as e:
            logger.error(f"Error updating sheets: {str(e)}")
    
    def _send_personalized_email(self, client_data: dict, score: int, category: str):
        """Generate and send personalized email."""
        try:
            email_result = self.chatgpt_service.generate_email(client_data, score, category)
            
            if email_result['success']:
                email_data = email_result['data']
                logger.info(f"Email generated for {client_data.get('nombre')}")
                # TODO: Implement email sending (integrate with Gmail API)
                
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
    
    def _reset_timeout(self, phone_number: str):
        """Reset the inactivity timeout for a user."""
        if phone_number in self.user_timeouts:
            self.user_timeouts[phone_number]['reset'] = True
    
    def start_timeout_monitor(self):
        """Start monitoring for inactive users."""
        def monitor():
            while True:
                time.sleep(60)  # Check every minute
                self._check_timeouts()
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
    
    def _check_timeouts(self):
        """Check for users with timeout."""
        # This would be implemented to send the Google Forms link
        # after 1 minute of inactivity
        pass

# Create singleton instance
_orchestrator = None

def get_chatbot_orchestrator():
    """Get or create chatbot orchestrator singleton."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = ChatbotOrchestrator()
    return _orchestrator
