"""
Configuration et initialisation de l'application Trading Agent.
"""

import sys
import os
from datetime import datetime

def setup_paths():
    """Configure les chemins d'accès pour les modules."""
    base_dir = os.path.dirname(os.path.dirname(__file__))  # Remonter au dossier parent
    paths_to_add = ['src', 'stocks', 'google_integration']
    
    for path in paths_to_add:
        full_path = os.path.join(base_dir, path)
        if os.path.exists(full_path):
            sys.path.insert(0, full_path)  # Utiliser insert(0) pour priorité
        else:
            print(f"⚠️  Attention: Le dossier '{path}' n'existe pas")

def import_modules():
    """Importe tous les modules nécessaires."""
    try:
        # Imports principaux
        from stocks.portfolio import GAFAM
        from stocks.get_data import get_stock_data
        from src.calculate_signals import calculate_signals
        from src.quick_analyze import analyze_quick
        from src.detailed_analyze import analyze_detailed
        
        # Import Google Sheets avec gestion d'erreur améliorée
        google_sheets_available = False
        GoogleSheetsManager = None
        GoogleSheetsInterface = None
        
        try:
            # Test d'abord si les dépendances Google sont disponibles
            import google.oauth2.service_account
            import googleapiclient.discovery
            
            # Si OK, importer nos modules
            from google_integration.sheets_manager import GoogleSheetsManager
            from google_integration.google_sheets import GoogleSheetsInterface
            
            google_sheets_available = True
            print("✅ Module Google Sheets chargé avec succès")
            
        except ImportError as e:
            print(f"⚠️  Google Sheets non disponible: {e}")
            print("💡 Pour activer Google Sheets, installez:")
            print("   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
            GoogleSheetsManager = None
            GoogleSheetsInterface = None
            google_sheets_available = False
        
        return {
            'GAFAM': GAFAM,
            'get_stock_data': get_stock_data,
            'calculate_signals': calculate_signals,
            'analyze_quick': analyze_quick,
            'analyze_detailed': analyze_detailed,
            'GoogleSheetsManager': GoogleSheetsManager,
            'GoogleSheetsInterface': GoogleSheetsInterface,
            'google_sheets_available': google_sheets_available
        }
        
    except ImportError as e:
        print(f"❌ Erreur d'import critique: {e}")
        print("💡 Vérifiez que tous les fichiers requis sont présents:")
        print("   - stocks/portfolio.py")
        print("   - stocks/get_data.py") 
        print("   - src/calculate_signals.py")
        print("   - src/quick_analyze.py")
        print("   - src/detailed_analyze.py")
        print("\n💡 Vérifiez aussi que les dépendances sont installées:")
        print("   pip install yfinance pandas")
        sys.exit(1)

def print_header():
    """Affiche l'en-tête de l'application."""
    print("=" * 80)
    print("🎯 TRADING AGENT SIMPLE")
    print("=" * 80)
    print("📊 Portefeuille: GAFAM")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

def check_dependencies():
    """Vérifie que les dépendances essentielles sont installées."""
    required_packages = ['yfinance', 'pandas']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Dépendances manquantes: {', '.join(missing_packages)}")
        print(f"💡 Installez avec: pip install {' '.join(missing_packages)}")
        return False
    
    return True

def initialize_app():
    """Initialise complètement l'application."""
    print("🚀 Démarrage de Trading Agent Simple...")
    
    # Vérifier les dépendances
    if not check_dependencies():
        sys.exit(1)
    
    # Configurer les chemins
    setup_paths()
    
    # Importer les modules
    modules = import_modules()
    
    # Afficher l'en-tête
    print_header()
    
    # Afficher le statut des modules
    print("📦 Modules chargés:")
    print(f"   ✅ Stocks: {bool(modules['GAFAM'])}")
    print(f"   ✅ Analyse: {bool(modules['analyze_quick'])}")
    print(f"   {'✅' if modules['google_sheets_available'] else '⚠️ '} Google Sheets: {modules['google_sheets_available']}")
    
    return modules
