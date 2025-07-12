"""
Formatage et styling des Google Sheets.
"""


class GoogleSheetsFormatter:
    
    @staticmethod
    def get_sheet_headers():
        """Définit les en-têtes pour la feuille de trading"""
        return [
            'Timestamp', 'Symbol', 'Company', 'Price ($)', 'RSI', 'MACD', 
            'Signals', 'Recommendation', 'Volume', 'Change (%)', 'Analysis Type'
        ]
    
    @staticmethod
    def get_header_formatting_requests(sheet_id, num_columns):
        """Génère les requêtes de formatage pour les en-têtes"""
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
    
    @staticmethod
    def get_sheet_structure_requests(sheet_id, num_columns):
        """Génère les requêtes de structure (auto-redimensionnement, gel, etc.)"""
        return [
            # Auto-redimensionnement des colonnes
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
            # Gel de la ligne d'en-tête
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
    
    @staticmethod
    def get_conditional_formatting_requests(sheet_id):
        """Génère les requêtes de formatage conditionnel pour les recommandations"""
        return [
            # Vert pour ACHETER
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
            # Rouge pour VENDRE
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
            # Jaune pour ATTENDRE
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
    
    @staticmethod
    def apply_sheet_formatting(service, sheet_id, sheet_name, headers):
        """Applique tout le formatage à une feuille"""
        try:
            sheet_internal_id = GoogleSheetsFormatter._get_sheet_id_by_name(
                service, sheet_id, sheet_name
            )
            if sheet_internal_id is None:
                print(f"⚠️  Impossible de trouver la feuille '{sheet_name}'")
                return False
            requests = []
            requests.extend(GoogleSheetsFormatter.get_header_formatting_requests(
                sheet_internal_id, len(headers)
            ))
            requests.extend(GoogleSheetsFormatter.get_sheet_structure_requests(
                sheet_internal_id, len(headers)
            ))
            requests.extend(GoogleSheetsFormatter.get_conditional_formatting_requests(
                sheet_internal_id
            ))
            service.spreadsheets().batchUpdate(
                spreadsheetId=sheet_id,
                body={'requests': requests}
            ).execute()
            print(f"✅ Formatage appliqué à '{sheet_name}'")
            return True
            
        except Exception as e:
            print(f"⚠️  Erreur formatage: {e}")
            return False
    
    @staticmethod
    def _get_sheet_id_by_name(service, spreadsheet_id, sheet_name):
        """Récupère l'ID interne de la feuille par son nom"""
        try:
            sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            sheets = sheet_metadata.get('sheets', [])
            
            for sheet in sheets:
                if sheet['properties']['title'] == sheet_name:
                    return sheet['properties']['sheetId']
            
            return None
            
        except Exception as e:
            print(f"❌ Erreur récupération Sheet ID: {e}")
            return None
