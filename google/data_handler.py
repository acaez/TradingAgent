"""
Gestion des données dans Google Sheets.
"""

from datetime import datetime


class GoogleDataHandler:
    
    def __init__(self, service, sheet_id):
        self.service = service
        self.sheet_id = sheet_id
    
    def append_analysis(self, symbol, analysis_data, analysis_type="Quick", sheet_name="Trading_Analysis"):
        if not self._validate_connection():
            return False
        
        try:
            row_data = self._prepare_analysis_row(symbol, analysis_data, analysis_type)
            
            if self._append_row_to_sheet(sheet_name, row_data):
                print(f"✅ Données ajoutées pour {symbol}")
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Erreur ajout données: {e}")
            return False
    
    def _prepare_analysis_row(self, symbol, analysis_data, analysis_type):
        return [
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            symbol,
            analysis_data.get('company', ''),
            analysis_data.get('price', ''),
            analysis_data.get('rsi', ''),
            analysis_data.get('macd', ''),
            analysis_data.get('signal', ''),
            analysis_data.get('recommendation', ''),
            analysis_data.get('volume', ''),
            analysis_data.get('change_percent', ''),
            analysis_type
        ]
    
    def _append_row_to_sheet(self, sheet_name, row_data):
        try:
            body = {'values': [row_data]}
            
            self.service.spreadsheets().values().append(
                spreadsheetId=self.sheet_id,
                range=f"{sheet_name}!A:K",
                valueInputOption='RAW',
                body=body
            ).execute()
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur ajout ligne: {e}")
            return False
    
    def update_range(self, range_name, values):
        if not self._validate_connection():
            return False
        
        try:
            body = {'values': values}
            
            self.service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur mise à jour: {e}")
            return False
    
    def get_sheet_data(self, range_name):
        if not self._validate_connection():
            return None
        
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range=range_name
            ).execute()
            
            return result.get('values', [])
            
        except Exception as e:
            print(f"❌ Erreur lecture données: {e}")
            return None
    
    def get_analysis_history(self, symbol=None, limit=10):
        try:
            all_data = self.get_sheet_data("Trading_Analysis!A:K")
            if not all_data or len(all_data) <= 1:
                return []
            data = all_data[1:]
            if symbol:
                data = [row for row in data if len(row) > 1 and row[1] == symbol]
            return data[-limit:] if len(data) > limit else data
            
        except Exception as e:
            print(f"❌ Erreur récupération historique: {e}")
            return []
    
    def _validate_connection(self):
        if not self.service or not self.sheet_id:
            print("❌ Service ou Sheet ID manquant")
            return False
        return True
