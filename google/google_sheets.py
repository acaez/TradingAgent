"""
Module principal Google Sheets - Compatibilité avec l'ancienne version.
"""

from .sheets_manager import GoogleSheetsManager
GoogleSheetsManager = GoogleSheetsManager

__all__ = ['GoogleSheetsManager']
