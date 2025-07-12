"""
Gestion de l'authentification Google Sheets.
"""

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


class GoogleAuth:
    
    def __init__(self, credentials_file='credentials.json'):
        self.credentials_file = credentials_file
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        try:
            scopes = ['https://www.googleapis.com/auth/spreadsheets']
            creds = Credentials.from_service_account_file(
                self.credentials_file, scopes=scopes
            )
            self.service = build('sheets', 'v4', credentials=creds)
            print("✅ Connexion Google Sheets réussie")
        except Exception as e:
            print(f"❌ Erreur authentification Google Sheets: {e}")
            raise
    
    def get_service(self):
        if not self.service:
            raise Exception("Service Google Sheets non initialisé")
        return self.service
    
    def is_authenticated(self):
        return self.service is not None
