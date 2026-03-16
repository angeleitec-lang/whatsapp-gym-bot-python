"""
ChatGPT Service for AI responses and client scoring
"""
import json

import openai

from config import Config
from logger import get_logger

logger = get_logger(__name__)

class ChatGPTService:
    """Service for OpenAI ChatGPT interactions."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        openai.api_key = self.config.OPENAI_API_KEY
    
    def get_response(self, message: str, context: str = None, conversation_history: list = None) -> dict:
        """
        Get a response from ChatGPT.
        
        Args:
            message: User message
            context: Additional context about the user
            conversation_history: List of previous messages
            
        Returns:
            Response from ChatGPT
        """
        try:
            messages = [
                {
                    "role": "system",
                    "content": """Eres un asistente amigable y profesional para Activate, un gimnasio especializado 
                    en entrenamiento personalizado de fuerza para personas de 50+ años. 
                    Tu objetivo es responder preguntas sobre el gimnasio, sus servicios, y proporcionar información útil 
                    sobre entrenamiento y bienestar. Siempre sé empático, respetuoso y enfocado en las necesidades del usuario."""
                }
            ]
            
            if context:
                messages.append({
                    "role": "system",
                    "content": f"Contexto del usuario: {context}"
                })
            
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({
                "role": "user",
                "content": message
            })
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            logger.info(f"ChatGPT response generated successfully")
            
            return {"success": True, "response": answer}
            
        except Exception as e:
            logger.error(f"Error getting ChatGPT response: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def score_client(self, client_data: dict) -> dict:
        """
        Score a client based on their information.
        
        Args:
            client_data: Dictionary with client information
            
        Returns:
            Scoring result with 0-100 score and category
        """
        try:
            prompt = f"""Analiza los siguientes datos del cliente y proporciona una puntuación de 0-100 
            basada en su potencial como cliente para un gimnasio especializado en entrenamiento de fuerza 
            personalizado para personas 50+:
            
            Datos del cliente:
            {json.dumps(client_data, indent=2, ensure_ascii=False)}
            
            Responde en formato JSON con:
            {{
                "score": <número 0-100>,
                "category": "<Frío|Tibio|Caliente>",
                "reasoning": "<explicación breve>",
                "recommendations": "<recomendaciones para mejorar la relación>"
            }}
            
            Criterios de puntuación:
            - 0-30: Frío (poco interés probable)
            - 31-69: Tibio (interés moderado)
            - 70-100: Caliente (alto potencial de conversión)"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un experto en análisis de leads para gimnasios."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=400
            )
            
            response_text = response.choices[0].message.content
            
            # Extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            json_str = response_text[start_idx:end_idx]
            
            scoring_result = json.loads(json_str)
            logger.info(f"Client scored successfully: {scoring_result['score']}")
            
            return {"success": True, "data": scoring_result}
            
        except Exception as e:
            logger.error(f"Error scoring client: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def generate_email(self, client_data: dict, score: int, category: str) -> dict:
        """
        Generate a personalized email for the client.
        
        Args:
            client_data: Dictionary with client information
            score: Client score
            category: Client category (Frío, Tibio, Caliente)
            
        Returns:
            Generated email with subject and body
        """
        try:
            prompt = f"""Genera un email personalizado para un cliente potencial de Activate (gimnasio de entrenamiento 
            personalizado para personas 50+).
            
            Datos del cliente:
            {json.dumps(client_data, indent=2, ensure_ascii=False)}
            
            Puntuación: {score}/100
            Categoría: {category}
            
            El email debe ser:
            - Personalizado con el nombre del cliente
            - Empático y respetuoso
            - Enfocado en sus necesidades específicas
            - Incluir una llamada a la acción clara
            
            Responde en formato JSON:
            {{
                "subject": "<asunto del email>",
                "body": "<cuerpo del email en HTML o texto>"
            }}"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un experto en copywriting para gimnasios."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            response_text = response.choices[0].message.content
            
            # Extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            json_str = response_text[start_idx:end_idx]
            
            email_result = json.loads(json_str)
            logger.info(f"Email generated successfully for client")
            
            return {"success": True, "data": email_result}
            
        except Exception as e:
            logger.error(f"Error generating email: {str(e)}")
            return {"success": False, "error": str(e)}

# Create singleton instance
_chatgpt_service = None

def get_chatgpt_service():
    """Get or create ChatGPT service singleton."""
    global _chatgpt_service
    if _chatgpt_service is None:
        _chatgpt_service = ChatGPTService()
    return _chatgpt_service
