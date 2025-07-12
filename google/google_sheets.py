import os
import json
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

class GoogleSheetsManager:
    def __init__(self, credentials_file='credentials.json'):
        self.credentials_file = credentials_file
        self.service = None
        self.sheet_id = None
        self._authenticate()
    
    # ========================
    # AUTHENTICATION METHODS
    # ========================
    
    def _authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            scopes = ['https://www.googleapis.com/auth/spreadsheets']
            creds = Credentials.from_service_account_file(
                self.credentials_file, scopes=scopes
            )
            self.service = build('sheets', 'v4', credentials=creds)
            print("✅ Connexion Google Sheets réussie")
        except Exception as e:
            print(f"❌ Erreur authentification Google Sheets: {e}")
    
    def set_spreadsheet(self, sheet_id):
        """Set the target spreadsheet ID"""
        self.sheet_id = sheet_id
        print(f"📋 Sheet ID configuré: {sheet_id}")
    
    # ========================
    # SHEET MANAGEMENT METHODS
    # ========================
    
    def create_trading_sheet(self, sheet_name="Trading_Analysis"):
        """Create a beautifully formatted trading analysis sheet"""
        if not self._validate_connection():
            return False
        
        try:
            headers = self._get_sheet_headers()
            
            # Create sheet structure
            if self._create_sheet_structure(sheet_name, headers):
                # Apply formatting
                self._format_sheet(sheet_name, headers)
                print(f"✅ Sheet '{sheet_name}' créée et formatée avec succès")
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Erreur création sheet: {e}")
            return False
    
    def _create_sheet_structure(self, sheet_name, headers):
        """Create the basic sheet structure"""
        try:
            # Try to create the sheet (ignore if already exists)
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
            # Sheet might already exist, that's ok
            print(f"ℹ️  Sheet '{sheet_name}' existe déjà")
        
        # Add headers regardless
        return self.update_range(f"{sheet_name}!A1:K1", [headers])
    
    def _get_sheet_headers(self):
        """Define the headers for the trading sheet"""
        return [
            'Timestamp', 'Symbol', 'Company', 'Price ($)', 'RSI', 'MACD', 
            'Signals', 'Recommendation', 'Volume', 'Change (%)', 'Analysis Type'
        ]
    
    # ========================
    # FORMATTING METHODS
    # ========================
    
    def _format_sheet(self, sheet_name, headers):
        """Apply beautiful formatting to the sheet"""
        try:
            sheet_id = self._get_sheet_id_by_name(sheet_name)
            if sheet_id is None:
                return
            
            # Apply all formatting
            requests = []
            requests.extend(self._get_header_formatting_requests(sheet_id, len(headers)))
            requests.extend(self._get_sheet_structure_requests(sheet_id, len(headers)))
            requests.extend(self._get_conditional_formatting_requests(sheet_id))
            
            # Execute all formatting requests
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.sheet_id,
                body={'requests': requests}
            ).execute()
            
            print(f"✅ Formatage appliqué à '{sheet_name}'")
            
        except Exception as e:
            print(f"⚠️  Erreur formatage: {e}")
    
    def _get_header_formatting_requests(self, sheet_id, num_columns):
        """Get formatting requests for headers"""
        return [{
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 0,
                    'endRowIndex': 1,
                    'startColumnIndex': 0,
                    'endColumnIndex': num_columns
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': {'red': 0.2, 'green': 0.6, 'blue': 1.0},
                        'textFormat': {
                            'foregroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0},
                            'fontSize': 12,
                            'bold': True
                        },
                        'horizontalAlignment': 'CENTER'
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
            }
        }]
    
    def _get_sheet_structure_requests(self, sheet_id, num_columns):
        """Get requests for sheet structure (auto-resize, freeze, etc.)"""
        return [
            # Auto-resize columns
            {
                'autoResizeDimensions': {
                    'dimensions': {
                        'sheetId': sheet_id,
                        'dimension': 'COLUMNS',
                        'startIndex': 0,
                        'endIndex': num_columns
                    }
                }
            },
            # Freeze header row
            {
                'updateSheetProperties': {
                    'properties': {
                        'sheetId': sheet_id,
                        'gridProperties': {
                            'frozenRowCount': 1
                        }
                    },
                    'fields': 'gridProperties.frozenRowCount'
                }
            }
        ]
    
    def _get_conditional_formatting_requests(self, sheet_id):
        """Get conditional formatting requests for recommendations"""
        return [
            # Green for ACHETER
            {
                'addConditionalFormatRule': {
                    'rule': {
                        'ranges': [{'sheetId': sheet_id, 'startColumnIndex': 7, 'endColumnIndex': 8}],
                        'booleanRule': {
                            'condition': {
                                'type': 'TEXT_CONTAINS',
                                'values': [{'userEnteredValue': 'ACHETER'}]
                            },
                            'format': {
                                'backgroundColor': {'red': 0.8, 'green': 1.0, 'blue': 0.8}
                            }
                        }
                    },
                    'index': 0
                }
            },
            # Red for VENDRE
            {
                'addConditionalFormatRule': {
                    'rule': {
                        'ranges': [{'sheetId': sheet_id, 'startColumnIndex': 7, 'endColumnIndex': 8}],
                        'booleanRule': {
                            'condition': {
                                'type': 'TEXT_CONTAINS',
                                'values': [{'userEnteredValue': 'VENDRE'}]
                            },
                            'format': {
                                'backgroundColor': {'red': 1.0, 'green': 0.8, 'blue': 0.8}
                            }
                        }
                    },
                    'index': 1
                }
            },
            # Yellow for ATTENDRE
            {
                'addConditionalFormatRule': {
                    'rule': {
                        'ranges': [{'sheetId': sheet_id, 'startColumnIndex': 7, 'endColumnIndex': 8}],
                        'booleanRule': {
                            'condition': {
                                'type': 'TEXT_CONTAINS',
                                'values': [{'userEnteredValue': 'ATTENDRE'}]
                            },
                            'format': {
                                'backgroundColor': {'red': 1.0, 'green': 1.0, 'blue': 0.8}
                            }
                        }
                    },
                    'index': 2
                }
            }
        ]
    
    # ========================
    # DATA MANIPULATION METHODS
    # ========================
    
    def append_analysis(self, symbol, analysis_data, analysis_type="Quick", sheet_name="Trading_Analysis"):
        """Append analysis data to the sheet"""
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
        """Prepare a row of data for insertion"""
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
        """Append a single row to the specified sheet"""
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
        """Update a specific range in the sheet"""
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
    
    # ========================
    # DATA RETRIEVAL METHODS
    # ========================
    
    def get_sheet_data(self, range_name):
        """Get data from a specific range"""
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
        """Get recent analysis history for a symbol or all symbols"""
        try:
            all_data = self.get_sheet_data("Trading_Analysis!A:K")
            
            if not all_data or len(all_data) <= 1:  # Only headers or empty
                return []
            
            # Skip headers
            data = all_data[1:]
            
            # Filter by symbol if specified
            if symbol:
                data = [row for row in data if len(row) > 1 and row[1] == symbol]
            
            # Return most recent entries
            return data[-limit:] if len(data) > limit else data
            
        except Exception as e:
            print(f"❌ Erreur récupération historique: {e}")
            return []
    
    # ========================
    # UTILITY METHODS
    # ========================
    
    def _validate_connection(self):
        """Validate that service and sheet_id are available"""
        if not self.service or not self.sheet_id:
            print("❌ Service ou Sheet ID manquant")
            return False
        return True
    
    def _get_sheet_id_by_name(self, sheet_name):
        """Get the internal sheet ID by sheet name"""
        try:
            sheet_metadata = self.service.spreadsheets().get(spreadsheetId=self.sheet_id).execute()
            sheets = sheet_metadata.get('sheets', [])
            
            for sheet in sheets:
                if sheet['properties']['title'] == sheet_name:
                    return sheet['properties']['sheetId']
            
            return None
            
        except Exception as e:
            print(f"❌ Erreur récupération Sheet ID: {e}")
            return None
    
    def get_sheet_info(self):
        """Get information about the current spreadsheet"""
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
        """Print formatted information about the current sheet"""
        info = self.get_sheet_info()
        
        if info:
            print(f"\n📊 INFORMATIONS GOOGLE SHEET:")
            print(f"   📋 Titre: {info['title']}")
            print(f"   📄 Onglets: {', '.join(info['sheets'])}")
            print(f"   🔗 URL: {info['url']}")
        else:
            print("❌ Impossible de récupérer les informations du sheet")
