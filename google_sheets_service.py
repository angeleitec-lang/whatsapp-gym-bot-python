"""
Google Sheets Service for spreadsheet operations
"""
import pickle
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from config import Config
from logger import get_logger

logger = get_logger(__name__)

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/forms'
]

class GoogleSheetsService:
    """Service for Google Sheets API operations."""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.service = None
        self.credentials = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Google using OAuth."""
        try:
            credentials = None
            
            # Load saved credentials if available
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    credentials = pickle.load(token)
            
            # Refresh credentials if expired
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            
            # If no valid credentials, get new ones
            if not credentials or not credentials.valid:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                credentials = flow.run_local_server(port=0)
                
                # Save credentials for future use
                with open('token.pickle', 'wb') as token:
                    pickle.dump(credentials, token)
            
            self.credentials = credentials
            self.service = build('sheets', 'v4', credentials=credentials)
            logger.info("Successfully authenticated with Google Sheets API")
            
        except Exception as e:
            logger.error(f"Error authenticating with Google Sheets: {str(e)}")
            self.service = None
    
    def append_row(self, values: list, sheet_id: str = None, range_name: str = None) -> bool:
        """
        Append a row to a Google Sheet.
        
        Args:
            values: List of values to append
            sheet_id: Google Sheet ID (uses config if not provided)
            range_name: Range to append to (uses config if not provided)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.service:
                self.authenticate()
            
            sheet_id = sheet_id or self.config.GOOGLE_SHEETS_ID
            range_name = range_name or self.config.GOOGLE_SHEETS_RANGE
            
            body = {
                'values': [values]
            }
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=sheet_id,
                range=range_name,
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            
            logger.info(f"Row appended successfully to {sheet_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error appending row to sheet: {str(e)}")
            return False
    
    def update_cell(self, row: int, col: int, value: str, sheet_id: str = None) -> bool:
        """
        Update a specific cell in a Google Sheet.
        
        Args:
            row: Row number (1-indexed)
            col: Column number (1-indexed)
            value: Value to set
            sheet_id: Google Sheet ID (uses config if not provided)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.service:
                self.authenticate()
            
            sheet_id = sheet_id or self.config.GOOGLE_SHEETS_ID
            
            # Convert to A1 notation
            col_letter = self._number_to_column_letter(col)
            cell_range = f"{col_letter}{row}"
            
            body = {
                'values': [[value]]
            }
            
            self.service.spreadsheets().values().update(
                spreadsheetId=sheet_id,
                range=cell_range,
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            
            logger.info(f"Cell {cell_range} updated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error updating cell: {str(e)}")
            return False
    
    def read_range(self, range_name: str, sheet_id: str = None) -> list:
        """
        Read values from a range in a Google Sheet.
        
        Args:
            range_name: Range to read (e.g., 'Sheet1!A1:D10')
            sheet_id: Google Sheet ID (uses config if not provided)
            
        Returns:
            List of lists with values
        """
        try:
            if not self.service:
                self.authenticate()
            
            sheet_id = sheet_id or self.config.GOOGLE_SHEETS_ID
            
            result = self.service.spreadsheets().values().get(
                spreadsheetId=sheet_id,
                range=range_name
            ).execute()
            
            return result.get('values', [])
            
        except Exception as e:
            logger.error(f"Error reading range: {str(e)}")
            return []
    
    def clear_range(self, range_name: str, sheet_id: str = None) -> bool:
        """
        Clear values from a range in a Google Sheet.
        
        Args:
            range_name: Range to clear
            sheet_id: Google Sheet ID (uses config if not provided)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.service:
                self.authenticate()
            
            sheet_id = sheet_id or self.config.GOOGLE_SHEETS_ID
            
            self.service.spreadsheets().values().clear(
                spreadsheetId=sheet_id,
                range=range_name
            ).execute()
            
            logger.info(f"Range {range_name} cleared successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing range: {str(e)}")
            return False
    
    @staticmethod
    def _number_to_column_letter(num: int) -> str:
        """Convert column number to letter (1=A, 2=B, etc.)."""
        result = ""
        while num > 0:
            num -= 1
            result = chr(65 + num % 26) + result
            num //= 26
        return result

# Create singleton instance
_sheets_service = None

def get_sheets_service():
    """Get or create Google Sheets service singleton."""
    global _sheets_service
    if _sheets_service is None:
        _sheets_service = GoogleSheetsService()
    return _sheets_service
