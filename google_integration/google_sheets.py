"""
Module principal Google Sheets - Interface simplifiée et utilitaires.
"""

from .sheets_manager import GoogleSheetsManager
from .auth import GoogleAuth
from .data_handler import GoogleDataHandler
from .formatter import GoogleSheetsFormatter
from .config import GoogleConfig


class GoogleSheetsInterface:
    
    def __init__(self, credentials_file='credentials.json'):
        self.manager = GoogleSheetsManager(credentials_file)
        self.is_configured = False
        self.sheet_info = None
    
    def setup_sheet(self, sheet_id, sheet_name="Trading_Analysis"):
        try:
            self.manager.set_spreadsheet(sheet_id)
            if self.manager.create_trading_sheet(sheet_name):
                self.is_configured = True
                self.sheet_info = self.manager.get_sheet_info()
                return True
            return False
            
        except Exception as e:
            print(f"❌ Erreur configuration sheet: {e}")
            return False
    
    def quick_add_analysis(self, symbol, price, decision, signals, volume=None, change_percent=None):
        if not self.is_configured:
            print("⚠️  Sheet non configuré")
            return False
        
        analysis_data = {
            'company': symbol,  # Sera remplacé par le nom si disponible
            'price': f"{price:.2f}",
            'rsi': 'N/A',
            'macd': 'N/A',
            'signal': ', '.join(signals) if isinstance(signals, list) else str(signals),
            'recommendation': decision,
            'volume': f"{volume:.0f}" if volume else 'N/A',
            'change_percent': f"{change_percent:.2f}%" if change_percent else 'N/A'
        }
        return self.manager.append_analysis(symbol, analysis_data, analysis_type="Quick")
    
    def append_analysis(self, symbol, analysis_data, analysis_type="Quick", sheet_name="Trading_Analysis"):
        """
        Méthode de compatibilité pour append_analysis.
        Redirige vers le manager.
        """
        if not self.is_configured:
            print("⚠️  Sheet non configuré")
            return False
        
        return self.manager.append_analysis(symbol, analysis_data, analysis_type, sheet_name)
    
    def get_trading_summary(self):
        if not self.is_configured:
            return None
        
        try:
            # Récupérer les 20 dernières analyses
            history = self.manager.get_analysis_history(limit=20)
            if not history:
                return None
            recommendations = {}
            for row in history:
                if len(row) > 7:
                    rec = row[7]
                    recommendations[rec] = recommendations.get(rec, 0) + 1
            return {
                'total_analyses': len(history),
                'recommendations': recommendations,
                'last_analysis': history[-1] if history else None
            }
            
        except Exception as e:
            print(f"❌ Erreur récupération résumé: {e}")
            return None
    
    def print_status(self):
        if not self.is_configured:
            print("📊 Google Sheets: Non configuré")
            return
        print("📊 Google Sheets: Configuré et prêt")
        if self.sheet_info:
            print(f"   📋 Titre: {self.sheet_info['title']}")
            print(f"   🔗 URL: {self.sheet_info['url']}")
        summary = self.get_trading_summary()
        if summary:
            print(f"   📈 Analyses totales: {summary['total_analyses']}")
            for rec, count in summary['recommendations'].items():
                print(f"   • {rec}: {count}")
    
    def export_to_csv(self, filename="trading_analysis.csv"):
        if not self.is_configured:
            print("⚠️  Sheet non configuré")
            return False
        
        try:
            import csv
            from datetime import datetime
            
            data = self.manager.get_sheet_data("Trading_Analysis!A:K")
            if not data:
                print("❌ Aucune donnée à exporter")
                return False
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"trading_analysis_{timestamp}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data)
            print(f"✅ Données exportées vers: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur export CSV: {e}")
            return False
    
    def clear_old_data(self, days_to_keep=30):
        """Supprime les données plus anciennes que X jours (fonctionnalité future)."""
        print("🔄 Nettoyage des anciennes données...")
        print(f"💡 Fonctionnalité à implémenter: garder {days_to_keep} jours")
        # TODO: Implémenter la suppression des anciennes données
        return True


# Fonctions utilitaires pour la compatibilité
def create_google_sheets_manager(credentials_file='credentials.json'):
    return GoogleSheetsManager(credentials_file)

def create_google_sheets_interface(credentials_file='credentials.json'):
    return GoogleSheetsInterface(credentials_file)

def test_google_connection(credentials_file='credentials.json'):
    try:
        auth = GoogleAuth(credentials_file)
        return auth.is_authenticated()
    except Exception as e:
        print(f"❌ Test connexion échoué: {e}")
        return False

__all__ = [
    'GoogleSheetsManager',
    'GoogleSheetsInterface', 
    'GoogleAuth',
    'GoogleDataHandler',
    'GoogleSheetsFormatter',
    'GoogleConfig',
    'create_google_sheets_manager',
    'create_google_sheets_interface',
    'test_google_connection'
]
