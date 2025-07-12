"""
Configuration et gestion de Google Sheets.
"""

def initialize_google_sheets(GoogleSheetsManager):
    
    if not GoogleSheetsManager:
        print("⚠️  Google Sheets non disponible")
        return None
    try:
        sheets_manager = GoogleSheetsManager()
        print("✅ Google Sheets prêt")
        return sheets_manager
    except Exception as e:
        print(f"⚠️  Erreur Google Sheets: {e}")
        return None

def configure_google_sheets(sheets_manager):
    
    if not sheets_manager:
        print("❌ Gestionnaire Google Sheets non disponible")
        return None
    print("\n📊 Configuration Google Sheets")
    while True:
        sheet_id = input("\n👉 ID de votre Google Sheet (ou 'skip' pour ignorer): ").strip()
        if sheet_id.lower() == 'skip':
            print("⏭️  Configuration Google Sheets ignorée")
            return None
        if not sheet_id:
            print("❌ Veuillez entrer un ID valide ou 'skip'")
            continue
        try:
            sheets_manager.set_spreadsheet(sheet_id)
            sheets_manager.create_trading_sheet()
            print("✅ Configuration Google Sheets terminée!")
            return sheets_manager
        except Exception as e:
            print(f"❌ Erreur lors de la configuration: {e}")
            retry = input("🔄 Voulez-vous réessayer? (y/n): ").strip().lower()
            if retry != 'y':
                print("⏭️  Configuration Google Sheets ignorée")
                return None

def setup_google_sheets_integration(modules):
    
    GoogleSheetsManager = modules.get('GoogleSheetsManager')
    sheets_manager = initialize_google_sheets(GoogleSheetsManager)
    if sheets_manager:
        configured_sheets = configure_google_sheets(sheets_manager)
        if configured_sheets:
            print("📝 Google Sheets configuré et prêt à utiliser")
            return configured_sheets
        else:
            print("📝 Fonctionnement sans Google Sheets")
            return None
    else:
        print("📝 Fonctionnement sans Google Sheets")
        return None
