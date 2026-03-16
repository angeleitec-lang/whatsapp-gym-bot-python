"""
WhatsApp Service for sending and receiving messages
"""
import json

import requests

from config import Config
from logger import get_logger

logger = get_logger(__name__)

class WhatsAppService:
    """Service for WhatsApp Business API interactions."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.api_url = self.config.WHATSAPP_API_URL
        self.phone_id = self.config.WHATSAPP_PHONE_ID
        self.access_token = self.config.WHATSAPP_ACCESS_TOKEN
        self.business_account_id = self.config.WHATSAPP_BUSINESS_ACCOUNT_ID
    
    def send_message(self, to_phone: str, message: str) -> dict:
        """
        Send a text message via WhatsApp.
        
        Args:
            to_phone: Phone number in E.164 format (e.g., +34612345678)
            message: Message text to send
            
        Returns:
            Response from WhatsApp API
        """
        try:
            url = f"{self.api_url}/{self.phone_id}/messages"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "messaging_product": "whatsapp",
                "to": to_phone,
                "type": "text",
                "text": {"body": message},
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code in [200, 201]:
                logger.info(f"Message sent successfully to {to_phone}")
                return {"success": True, "data": response.json()}
            else:
                logger.error(f"Failed to send message: {response.text}")
                return {"success": False, "error": response.text}
                
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def send_media_message(self, to_phone: str, media_url: str, media_type: str) -> dict:
        """
        Send a media message (image, video, document) via WhatsApp.
        
        Args:
            to_phone: Phone number in E.164 format
            media_url: URL of the media
            media_type: Type of media (image, video, document, audio)
            
        Returns:
            Response from WhatsApp API
        """
        try:
            url = f"{self.api_url}/{self.phone_id}/messages"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "messaging_product": "whatsapp",
                "to": to_phone,
                "type": media_type,
                media_type: {"link": media_url},
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code in [200, 201]:
                logger.info(f"Media message sent successfully to {to_phone}")
                return {"success": True, "data": response.json()}
            else:
                logger.error(f"Failed to send media message: {response.text}")
                return {"success": False, "error": response.text}
                
        except Exception as e:
            logger.error(f"Error sending media message: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def send_template_message(self, to_phone: str, template_name: str, params: list = None) -> dict:
        """
        Send a pre-approved template message.
        
        Args:
            to_phone: Phone number in E.164 format
            template_name: Name of the template
            params: List of parameters for the template
            
        Returns:
            Response from WhatsApp API
        """
        try:
            url = f"{self.api_url}/{self.phone_id}/messages"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "messaging_product": "whatsapp",
                "to": to_phone,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {"code": "es"}
                }
            }
            
            if params:
                payload["template"]["parameters"] = {"body": {"parameters": params}}
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code in [200, 201]:
                logger.info(f"Template message sent successfully to {to_phone}")
                return {"success": True, "data": response.json()}
            else:
                logger.error(f"Failed to send template message: {response.text}")
                return {"success": False, "error": response.text}
                
        except Exception as e:
            logger.error(f"Error sending template message: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def mark_message_read(self, message_id: str) -> dict:
        """
        Mark a received message as read.
        
        Args:
            message_id: ID of the message to mark as read
            
        Returns:
            Response from WhatsApp API
        """
        try:
            url = f"{self.api_url}/{self.phone_id}/messages"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            }
            
            payload = {
                "messaging_product": "whatsapp",
                "status": "read",
                "message_id": message_id,
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code in [200, 201]:
                logger.info(f"Message marked as read: {message_id}")
                return {"success": True}
            else:
                logger.error(f"Failed to mark message as read: {response.text}")
                return {"success": False, "error": response.text}
                
        except Exception as e:
            logger.error(f"Error marking message as read: {str(e)}")
            return {"success": False, "error": str(e)}

# Create singleton instance
_whatsapp_service = None

def get_whatsapp_service():
    """Get or create WhatsApp service singleton."""
    global _whatsapp_service
    if _whatsapp_service is None:
        _whatsapp_service = WhatsAppService()
    return _whatsapp_service
