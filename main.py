#!/usr/bin/env python3

import sys
import os
from datetime import datetime

# Ajouter les dossiers au path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'stocks'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'google'))  # Ajout du dossier google

try:
    # Import des modules
    from stocks.portfolio import GAFAM
    from stocks.get_data import get_stock_data
    from src.calculate_signals import calculate_signals
    from src.quick_analyze import analyze_quick
    from src.detailed_analyze import analyze_detailed
    
    # Try to import Google Sheets - CORRECTION ICI
    try:
        from google_sheets import GoogleSheetsManager  # Pas de préfixe google.
        GOOGLE_SHEETS_AVAILABLE = True
    except ImportError:
        print("⚠️  Google Sheets non disponible")
        GOOGLE_SHEETS_AVAILABLE = False
        
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print("💡 Vérifiez que tous les fichiers sont présents")
    sys.exit(1)

def main():
    print("=" * 60)
    print("🎯 TRADING AGENT SIMPLE")
    print("=" * 60)
    print("📊 Portefeuille: GAFAM")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Initialize Google Sheets if available
    sheets_manager = None
    if GOOGLE_SHEETS_AVAILABLE:
        try:
            sheets_manager = GoogleSheetsManager()
            print("✅ Google Sheets prêt")
        except Exception as e:
            print(f"⚠️  Google Sheets erreur: {e}")
    
    print("\nQue voulez-vous faire ?")
    print("1. 🚀 Analyse rapide (toutes les actions)")
    print("2. 🔍 Analyse détaillée (une action)")
    if GOOGLE_SHEETS_AVAILABLE:
        print("3. 📊 Configurer Google Sheets")
        print("4. ❌ Quitter")
    else:
        print("3. ❌ Quitter")
    
    while True:
        try:
            max_choice = 4 if GOOGLE_SHEETS_AVAILABLE else 3
            choice = input(f"\n👉 Votre choix (1-{max_choice}): ").strip()
            
            if choice == '1':
                print()
                analyze_quick(sheets_manager)
                
            elif choice == '2':
                print("\n📋 Actions disponibles:")
                for symbol, name in GAFAM.items():
                    print(f"   • {symbol}: {name}")
                
                symbol = input("\n👉 Symbole à analyser: ").strip().upper()
                print()
                analyze_detailed(symbol, sheets_manager)  # CORRECTION: Passer sheets_manager
                
            elif choice == '3' and GOOGLE_SHEETS_AVAILABLE:
                print("\n📊 Configuration Google Sheets")
                print("💡 Étapes:")
                print("1. Créez un Google Sheet")
                print("2. Partagez-le avec: workflow-trading-bot@warm-cycle-465007-c5.iam.gserviceaccount.com")
                print("3. Copiez l'ID depuis l'URL")
                
                if sheets_manager:
                    sheet_id = input("\n👉 ID de votre Google Sheet: ").strip()
                    if sheet_id:
                        sheets_manager.set_spreadsheet(sheet_id)
                        sheets_manager.create_trading_sheet()
                        print("✅ Configuration terminée!")
                    else:
                        print("❌ ID invalide")
                
            elif (choice == '3' and not GOOGLE_SHEETS_AVAILABLE) or (choice == '4' and GOOGLE_SHEETS_AVAILABLE):
                print("\n👋 Au revoir !")
                break
                
            else:
                print(f"❌ Choix invalide, tapez 1 à {max_choice}")
                
            if choice in ['1', '2']:
                continue_choice = input("\n🔄 Continuer ? (Y/n): ").strip().lower()
                if continue_choice in ['n', 'non', 'no']:
                    print("\n👋 Au revoir !")
                    break
                elif continue_choice in ['y', 'yes', 'oui', '']:
                    print("\nQue voulez-vous faire ?")
                    print("1. 🚀 Analyse rapide (toutes les actions)")
                    print("2. 🔍 Analyse détaillée (une action)")
                    if GOOGLE_SHEETS_AVAILABLE:
                        print("3. 📊 Configurer Google Sheets")
                        print("4. ❌ Quitter")
                    else:
                        print("3. ❌ Quitter")
                    
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir !")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()