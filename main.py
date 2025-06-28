#!/usr/bin/env python3
"""
Système d'analyse technique boursière
=====================================

Fichier principal qui combine l'analyse des signaux et la visualisation graphique.

Modules requis:
- trading_signals.py : Analyse des signaux de trading
- stock_charts.py : Visualisation graphique
- utils.py : Fonctions utilitaires

Usage:
    python main.py
"""

from trading_signals import analyze_multiple_stocks, STOCKS
from utils import initialize_utils, create_summary_stats, print_summary_stats, export_results_to_csv

def main():
    """
    Fonction principale qui execute l'analyse complète
    """
    # Initialisation
    initialize_utils()
    
    print("🚀 SYSTÈME D'ANALYSE TECHNIQUE BOURSIÈRE")
    print("=" * 50)
    print("📅 Période d'analyse: 2024")
    print(f"📊 Actions analysées: {len(STOCKS)} actions")
    print("=" * 50)
    
    # Étape 1: Analyse des signaux de trading
    print("\n🔍 ÉTAPE 1: ANALYSE DES SIGNAUX DE TRADING")
    print("-" * 50)
    results_df = analyze_multiple_stocks()
    
    if results_df.empty:
        print("❌ Aucune donnée analysée. Arrêt du programme.")
        return
    
    # Affichage des statistiques
    stats = create_summary_stats(results_df)
    print_summary_stats(stats)
    
    # Menu interactif
    while True:
        try:
            print("\n" + "=" * 50)
            print("🎯 MENU PRINCIPAL")
            print("=" * 50)
            print("1. 📈 Afficher le résumé des résultats")
            print("2. 🔍 Analyser une action spécifique")
            print("3. 💾 Exporter les résultats vers CSV")
            print("4. ✅ Quitter")
            
            choice = input("\nChoisissez une option (1-4): ").strip()
            
            if choice == '1':
                print("\n📊 RÉSUMÉ DES RÉSULTATS:")
                print_summary_stats(stats)
                
            elif choice == '2':
                print("\n🔍 ANALYSE D'UNE ACTION SPÉCIFIQUE:")
                print("Actions disponibles:", ", ".join(STOCKS.keys()))
                symbol = input("Entrez le symbole (ex: AAPL): ").strip().upper()
                if symbol in STOCKS:
                    single_result = results_df[results_df['Symbol'] == symbol]
                    if not single_result.empty:
                        row = single_result.iloc[0]
                        print(f"\n📈 {row['Name']} ({row['Symbol']}):")
                        print(f"   Prix actuel: ${row['Price']:.2f}")
                        print(f"   MA20: ${row['MA20']:.2f}")
                        print(f"   MA50: ${row['MA50']:.2f}")
                        print(f"   Signaux haussiers: {row['Bullish_Signals']}/3")
                        print(f"   Signal: {row['Signal']}")
                    else:
                        print(f"❌ Aucune donnée trouvée pour {symbol}")
                else:
                    print(f"❌ Symbole {symbol} non reconnu")
                    
            elif choice == '3':
                print("\n💾 Export des résultats...")
                filename = export_results_to_csv(results_df)
                if filename:
                    print(f"📁 Fichier créé: {filename}")
                    
            elif choice == '4':
                print("\n✅ Programme terminé. Merci d'avoir utilisé le système d'analyse!")
                break
                
            else:
                print("❌ Option invalide. Veuillez choisir entre 1 et 4.")
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Programme interrompu par l'utilisateur.")
            break
        except Exception as e:
            print(f"❌ Erreur inattendue: {str(e)}")

def quick_analysis():
    """
    Fonction pour une analyse rapide sans menu interactif
    """
    print("⚡ ANALYSE RAPIDE")
    print("=" * 30)
    
    # Analyse des signaux
    results_df = analyze_multiple_stocks()
    
    if not results_df.empty:
        # Affichage des statistiques rapides
        stats = create_summary_stats(results_df)
        print_summary_stats(stats)
    
    print("\n✅ Analyse rapide terminée!")

def custom_analysis():
    """
    Fonction pour une analyse personnalisée avec paramètres customisés
    """
    print("🔧 ANALYSE PERSONNALISÉE")
    print("=" * 30)
    
    # Saisie des paramètres personnalisés
    try:
        start_date = input("Date de début (YYYY-MM-DD) [défaut: 2024-01-01]: ").strip()
        if not start_date:
            start_date = "2024-01-01"
            
        end_date = input("Date de fin (YYYY-MM-DD) [défaut: 2024-12-31]: ").strip()
        if not end_date:
            end_date = "2024-12-31"
        
        print(f"\n📅 Période sélectionnée: {start_date} à {end_date}")
        
        # Actions personnalisées (optionnel)
        custom_stocks = input("\nActions à analyser (ex: AAPL,TSLA,GOOGL) [défaut: toutes]: ").strip()
        
        if custom_stocks:
            # Conversion en dictionnaire
            symbols = [s.strip().upper() for s in custom_stocks.split(',')]
            stocks_dict = {}
            for symbol in symbols:
                if symbol in STOCKS:
                    stocks_dict[symbol] = STOCKS[symbol]
                else:
                    stocks_dict[symbol] = symbol  # Utilise le symbole comme nom si inconnu
            
            print(f"📊 Actions sélectionnées: {list(stocks_dict.keys())}")
            results_df = analyze_multiple_stocks(stocks_dict, start_date, end_date)
        else:
            results_df = analyze_multiple_stocks(start_date=start_date, end_date=end_date)
        
        # Affichage des résultats
        if not results_df.empty:
            stats = create_summary_stats(results_df)
            print_summary_stats(stats)
            print("✅ Analyse personnalisée terminée!")
        else:
            print("❌ Aucune donnée analysée.")
            
    except Exception as e:
        print(f"❌ Erreur dans l'analyse personnalisée: {str(e)}")

if __name__ == "__main__":
    # Menu principal
    print("🎯 MODES D'ANALYSE DISPONIBLES")
    print("=" * 40)
    print("1. 🔍 Analyse complète (avec menu interactif)")
    print("2. ⚡ Analyse rapide (automatique)")
    print("3. 🔧 Analyse personnalisée (paramètres custom)")
    
    try:
        mode = input("\nChoisissez un mode (1-3): ").strip()
        
        if mode == '1':
            main()
        elif mode == '2':
            quick_analysis()
        elif mode == '3':
            custom_analysis()
        else:
            print("❌ Mode invalide. Lancement du mode par défaut...")
            main()
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Programme interrompu.")
    except Exception as e:
        print(f"❌ Erreur au démarrage: {str(e)}")
        print("🔄 Lancement du mode par défaut...")
        main()