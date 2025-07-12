"""
Système de menu pour l'application Trading Agent.
"""

def display_menu():
    print("\n" + "=" * 80)
    print("🎯 QUE VOULEZ-VOUS FAIRE ?")
    print("=" * 80)
    print("1. 🚀 Analyse rapide (toutes les actions)")
    print("2. 🔍 Analyse détaillée (une action)")
    print("3. ❌ Quitter")
    print("=" * 50)

def get_user_choice():
    
    while True:
        try:
            choice = input("\n👉 Votre choix (1-3): ").strip()
            if choice in ['1', '2', '3']:
                return choice
            else:
                print("❌ Choix invalide. Veuillez entrer 1, 2 ou 3.")
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir !")
            return '3'  # Traiter Ctrl+C comme quitter
        except Exception as e:
            print(f"❌ Erreur: {e}")
            print("💡 Veuillez entrer un nombre entre 1 et 3.")

def handle_quick_analysis(analyze_quick, sheets_manager):
    
    print("\n🚀 Démarrage de l'analyse rapide...")
    try:
        analyze_quick(sheets_manager)
        print("✅ Analyse rapide terminée!")
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse rapide: {e}")

def handle_detailed_analysis(analyze_detailed, GAFAM, sheets_manager):
    
    print("\n🔍 Analyse détaillée")
    print("=" * 80)
    print("📋 Actions disponibles:")
    for symbol, name in GAFAM.items():
        print(f"   • {symbol}: {name}")
    while True:
        symbol = input("\n👉 Symbole à analyser: ").strip().upper()
        if not symbol:
            print("❌ Veuillez entrer un symbole.")
            continue
        if symbol in GAFAM:
            print(f"\n🔍 Analyse détaillée de {symbol} ({GAFAM[symbol]})...")
            try:
                analyze_detailed(symbol, sheets_manager)
                print("✅ Analyse détaillée terminée!")
                break
            except Exception as e:
                print(f"❌ Erreur lors de l'analyse de {symbol}: {e}")
                retry = input("🔄 Voulez-vous réessayer avec un autre symbole? (y/n): ").strip().lower()
                if retry != 'y':
                    break
        else:
            print(f"❌ Symbole '{symbol}' non trouvé.")
            print("💡 Symboles disponibles:", ", ".join(GAFAM.keys()))
            retry = input("🔄 Voulez-vous réessayer? (y/n): ").strip().lower()
            if retry != 'y':
                break

def run_main_menu(modules, sheets_manager):
    
    print("\n🎯 Application prête à utiliser!")
    analyze_quick = modules['analyze_quick']
    analyze_detailed = modules['analyze_detailed']
    GAFAM = modules['GAFAM']
    while True:
        display_menu()
        choice = get_user_choice()
        if choice == '1':
            handle_quick_analysis(analyze_quick, sheets_manager)
        elif choice == '2':
            handle_detailed_analysis(analyze_detailed, GAFAM, sheets_manager)
        elif choice == '3':
            print("\n👋 Au revoir !")
            break
        if choice in ['1', '2']:
            print("\n" + "-" * 80)
            continue_choice = input("🔄 Voulez-vous faire autre chose? (y/n): ").strip().lower()
            if continue_choice != 'y':
                print("\n👋 Au revoir !")
                break
