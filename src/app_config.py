"""
Configuration et initialisation de l'application Trading Agent.
"""

import sys
import os
from datetime import datetime

def setup_paths():
    
    base_dir = os.path.dirname(os.path.dirname(__file__))  # Remonter au dossier parent
    paths_to_add = ['src', 'stocks', 'google']
    for path in paths_to_add:
        full_path = os.path.join(base_dir, path)
        if os.path.exists(full_path):
            sys.path.append(full_path)
        else:
            print(f"⚠️  Attention: Le dossier '{path}' n'existe pas")

def import_modules():
    try:
        from stocks.portfolio import GAFAM
        from stocks.get_data import get_stock_data
        from src.calculate_signals import calculate_signals
        from src.quick_analyze import analyze_quick
        from src.detailed_analyze import analyze_detailed
        try:
            from google_sheets import GoogleSheetsManager
            google_sheets_available = True
            print("✅ Module Google Sheets chargé avec succès")
        except ImportError:
            GoogleSheetsManager = None
            google_sheets_available = False
            print("⚠️  Google Sheets non disponible (optionnel)")
        return {
            'GAFAM': GAFAM,
            'get_stock_data': get_stock_data,
            'calculate_signals': calculate_signals,
            'analyze_quick': analyze_quick,
            'analyze_detailed': analyze_detailed,
            'GoogleSheetsManager': GoogleSheetsManager,
            'google_sheets_available': google_sheets_available
        }
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("💡 Vérifiez que tous les fichiers requis sont présents:")
        print("   - stocks/portfolio.py")
        print("   - stocks/get_data.py") 
        print("   - src/calculate_signals.py")
        print("   - src/quick_analyze.py")
        print("   - src/detailed_analyze.py")
        sys.exit(1)

def print_header():
    
    print("=" * 80)
    print("🎯 TRADING AGENT SIMPLE")
    print("=" * 80)
    print("📊 Portefeuille: GAFAM")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

def initialize_app():
    
    print("🚀 Démarrage de Trading Agent Simple...")
    setup_paths()
    modules = import_modules()
    print_header()
    return modules
