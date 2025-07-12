"""
Configuration pour Google Sheets.
"""


class GoogleConfig:
    
    DEFAULT_CREDENTIALS_FILE = 'credentials.json'
    DEFAULT_SHEET_NAME = 'Trading_Analysis'
    GOOGLE_SHEETS_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    TRADING_COLUMNS = {
        'TIMESTAMP': 0,
        'SYMBOL': 1,
        'COMPANY': 2,
        'PRICE': 3,
        'RSI': 4,
        'MACD': 5,
        'SIGNALS': 6,
        'RECOMMENDATION': 7,
        'VOLUME': 8,
        'CHANGE_PERCENT': 9,
        'ANALYSIS_TYPE': 10
    }
    COLORS = {
        'HEADER_BACKGROUND': {'red': 0.2, 'green': 0.6, 'blue': 1.0},
        'HEADER_TEXT': {'red': 1.0, 'green': 1.0, 'blue': 1.0},
        'BUY_BACKGROUND': {'red': 0.8, 'green': 1.0, 'blue': 0.8},
        'SELL_BACKGROUND': {'red': 1.0, 'green': 0.8, 'blue': 0.8},
        'WAIT_BACKGROUND': {'red': 1.0, 'green': 1.0, 'blue': 0.8}
    }
    RECOMMENDATION_KEYWORDS = {
        'BUY': 'ACHETER',
        'SELL': 'VENDRE',
        'WAIT': 'ATTENDRE'
    }
    @staticmethod
    def get_sheet_url(sheet_id):
        return f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
    
    @staticmethod
    def get_range_name(sheet_name, start_col='A', end_col='K'):
        return f"{sheet_name}!{start_col}:{end_col}"
