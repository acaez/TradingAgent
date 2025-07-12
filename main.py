#!/usr/bin/env python3

from src.app_config import initialize_app
from src.google_sheets_config import setup_google_sheets_integration
from src.menu_system import run_main_menu

def main():
    
    try:
        modules = initialize_app()
        sheets_manager = setup_google_sheets_integration(modules)
        run_main_menu(modules, sheets_manager)
    except KeyboardInterrupt:
        print("\n\n👋 Au revoir !")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        print("💡 Veuillez redémarrer l'application.")

if __name__ == "__main__":
    main()
