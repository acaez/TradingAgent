"""
Système de menu pour l'application Trading Agent.
"""

def select_portfolio(modules):
    """Permet à l'utilisateur de sélectionner un portefeuille."""
    portfolios = {
        '1': ('PERSO', modules['PERSO']),
        '2': ('BIGPHARMA', modules['BIGPHARMA']),
        '3': ('SMALLPHARMA', modules['SMALLPHARMA'])
    }
    
    print("\n" + "=" * 80)
    print("📊 SÉLECTION DU PORTEFEUILLE")
    print("=" * 80)
    print("1. 🏠 PERSO (Portfolio personnel)")
    print("2. 💊 BIGPHARMA (Grandes pharmas)")
    print("3. 🧪 SMALLPHARMA (Petites pharmas)")
    print("=" * 50)
    
    while True:
        try:
            choice = input("\n👉 Choisissez votre portefeuille (1-3): ").strip()
            if choice in portfolios:
                name, portfolio = portfolios[choice]
                print(f"✅ Portefeuille sélectionné: {name} ({len(portfolio)} actions)")
                return name, portfolio
            else:
                print("❌ Choix invalide. Veuillez entrer 1, 2 ou 3.")
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir !")
            return None, None
        except Exception as e:
            print(f"❌ Erreur: {e}")

def display_menu():
    print("\n" + "=" * 80)
    print("🎯 QUE VOULEZ-VOUS FAIRE ?")
    print("=" * 80)
    print("1. 🚀 Analyse rapide (toutes les actions)")
    print("2. 🔍 Analyse détaillée (une action)")
    print("3. 🔄 Changer de portefeuille")
    print("4. ❌ Quitter")
    print("=" * 50)

def get_user_choice():
    
    while True:
        try:
            choice = input("\n👉 Votre choix (1-4): ").strip()
            if choice in ['1', '2', '3', '4']:
                return choice
            else:
                print("❌ Choix invalide. Veuillez entrer 1, 2, 3 ou 4.")
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir !")
            return '4'  # Traiter Ctrl+C comme quitter
        except Exception as e:
            print(f"❌ Erreur: {e}")
            print("💡 Veuillez entrer un nombre entre 1 et 4.")

def handle_quick_analysis(analyze_quick, portfolio_name, portfolio, sheets_manager):
    
    print(f"\n🚀 Démarrage de l'analyse rapide pour {portfolio_name}...")
    try:
        analyze_quick(portfolio_name, portfolio, sheets_manager)
        print("✅ Analyse rapide terminée!")
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse rapide: {e}")

def handle_detailed_analysis(analyze_detailed, portfolio_name, portfolio, sheets_manager):
    
    print(f"\n🔍 Analyse détaillée - {portfolio_name}")
    print("=" * 80)
    print("📋 Actions disponibles:")
    for symbol, name in portfolio.items():
        print(f"   • {symbol}: {name}")
    while True:
        symbol = input("\n👉 Symbole à analyser: ").strip().upper()
        if not symbol:
            print("❌ Veuillez entrer un symbole.")
            continue
        if symbol in portfolio:
            print(f"\n🔍 Analyse détaillée de {symbol} ({portfolio[symbol]})...")
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
            print("💡 Symboles disponibles:", ", ".join(portfolio.keys()))
            retry = input("🔄 Voulez-vous réessayer? (y/n): ").strip().lower()
            if retry != 'y':
                break

def run_main_menu(modules, sheets_manager):
    
    print("\n🎯 Application prête à utiliser!")
    analyze_quick = modules['analyze_quick']
    analyze_detailed = modules['analyze_detailed']
    
    # Sélection initiale du portefeuille
    portfolio_name, portfolio = select_portfolio(modules)
    if portfolio is None:
        return
    
    while True:
        display_menu()
        choice = get_user_choice()
        if choice == '1':
            handle_quick_analysis(analyze_quick, portfolio_name, portfolio, sheets_manager)
        elif choice == '2':
            handle_detailed_analysis(analyze_detailed, portfolio_name, portfolio, sheets_manager)
        elif choice == '3':
            portfolio_name, portfolio = select_portfolio(modules)
            if portfolio is None:
                break
            continue
        elif choice == '4':
            print("\n👋 Au revoir !")
            break
        if choice in ['1', '2']:
            print("\n" + "-" * 80)
            continue_choice = input("🔄 Voulez-vous faire autre chose? (y/n): ").strip().lower()
            if continue_choice != 'y':
                print("\n👋 Au revoir !")
                break
