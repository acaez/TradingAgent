#!/usr/bin/env python3

import sys
import os
from datetime import datetime

# Ajouter les dossiers au path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'stocks'))

try:
    # Import des modules
    from stocks.portfolio import GAFAM
    from stocks.get_data import get_stock_data
    from src.calculate_signals import calculate_signals
    from src.quick_analyze import analyze_quick
    from src.detailed_analyze import analyze_detailed
    
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
    
    print("\nQue voulez-vous faire ?")
    print("1. 🚀 Analyse rapide (toutes les actions)")
    print("2. 🔍 Analyse détaillée (une action)")
    print("3. ❌ Quitter")
    
    while True:
        try:
            choice = input("\n👉 Votre choix (1-3): ").strip()
            
            if choice == '1':
                print()
                analyze_quick()
                
            elif choice == '2':
                print("\n📋 Actions disponibles:")
                for symbol, name in GAFAM.items():
                    print(f"   • {symbol}: {name}")
                
                symbol = input("\n👉 Symbole à analyser: ").strip().upper()
                print()
                analyze_detailed(symbol)
                
            elif choice == '3':
                print("\n👋 Au revoir !")
                break
                
            else:
                print("❌ Choix invalide, tapez 1, 2 ou 3")
                
            if choice in ['1', '2']:
                continue_choice = input("\n🔄 Continuer ? (Y/n): ").strip().lower()
                if continue_choice in ['n', 'non', 'no']:
                    print("\n👋 Au revoir !")
                    break
                elif continue_choice in ['y', 'yes', 'oui', '']:
                    print("\nQue voulez-vous faire ?")
                    print("1. 🚀 Analyse rapide (toutes les actions)")
                    print("2. 🔍 Analyse détaillée (une action)")
                    print("3. ❌ Quitter")
                
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir !")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()
