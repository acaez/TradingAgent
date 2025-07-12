"""
Gestionnaire principal pour Google Sheets.
"""

from .auth import GoogleAuth
from .data_handler import GoogleDataHandler
from .formatter import GoogleSheetsFormatter


class GoogleSheetsManager:
    
    def __init__(self, credentials_file='credentials.json'):
        self.auth = GoogleAuth(credentials_file)
        self.service = self.auth.get_service()
        self.sheet_id = None
        self.data_handler = None
    
    def set_spreadsheet(self, sheet_id):
        self.sheet_id = sheet_id
        self.data_handler = GoogleDataHandler(self.service, sheet_id)
        print(f"📋 Sheet ID configuré: {sheet_id}")
    
    def create_trading_sheet(self, sheet_name="Trading_Analysis"):
        if not self._validate_connection():
            return False
        
        try:
            headers = GoogleSheetsFormatter.get_sheet_headers()
            
            # Créer la structure de la feuille
            if self._create_sheet_structure(sheet_name, headers):
                # Appliquer le formatage
                GoogleSheetsFormatter.apply_sheet_formatting(
                    self.service, self.sheet_id, sheet_name, headers
                )
                print(f"✅ Sheet '{sheet_name}' créée et formatée avec succès")
                return True
            return False
            
        except Exception as e:
            print(f"❌ Erreur création sheet: {e}")
            return False
    
    def _create_sheet_structure(self, sheet_name, headers):
        try:
            # Essayer de créer la feuille (ignorer si elle existe déjà)
            body = {
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': sheet_name,
                            'gridProperties': {
                                'rowCount': 1000,
                                'columnCount': len(headers)
                            }
                        }
                    }
                }]
            }
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.sheet_id,
                body=body
            ).execute()
            print(f"✅ Structure de '{sheet_name}' créée")
            
        except Exception as e:
            # La feuille existe peut-être déjà, c'est OK
            print(f"ℹ️  Sheet '{sheet_name}' existe déjà")
        return self.data_handler.update_range(f"{sheet_name}!A1:K1", [headers])
    
    def append_analysis(self, symbol, analysis_data, analysis_type="Quick", sheet_name="Trading_Analysis"):
        if not self.data_handler:
            print("❌ Gestionnaire de données non initialisé")
            return False
        return self.data_handler.append_analysis(symbol, analysis_data, analysis_type, sheet_name)
    
    def get_sheet_data(self, range_name):
        if not self.data_handler:
            print("❌ Gestionnaire de données non initialisé")
            return None
        return self.data_handler.get_sheet_data(range_name)
    
    def get_analysis_history(self, symbol=None, limit=10):
        if not self.data_handler:
            print("❌ Gestionnaire de données non initialisé")
            return []
        return self.data_handler.get_analysis_history(symbol, limit)
    
    def update_range(self, range_name, values):
        if not self.data_handler:
            print("❌ Gestionnaire de données non initialisé")
            return False
        return self.data_handler.update_range(range_name, values)
    
    def get_sheet_info(self):
        if not self._validate_connection():
            return None
        try:
            sheet_metadata = self.service.spreadsheets().get(spreadsheetId=self.sheet_id).execute()
            
            info = {
                'title': sheet_metadata['properties']['title'],
                'sheets': [sheet['properties']['title'] for sheet in sheet_metadata.get('sheets', [])],
                'url': f"https://docs.google.com/spreadsheets/d/{self.sheet_id}/edit"
            }
            return info
            
        except Exception as e:
            print(f"❌ Erreur récupération info: {e}")
            return None
    
    def print_sheet_info(self):
        info = self.get_sheet_info()
        
        if info:
            print(f"\n📊 INFORMATIONS GOOGLE SHEET:")
            print(f"   📋 Titre: {info['title']}")
            print(f"   📄 Onglets: {', '.join(info['sheets'])}")
            print(f"   🔗 URL: {info['url']}")
        else:
            print("❌ Impossible de récupérer les informations du sheet")
    
    def _validate_connection(self):
        if not self.service or not self.sheet_id:
            print("❌ Service ou Sheet ID manquant")
            return False
        return True
