"""
Configuration et gestion de Google Sheets - Version améliorée.
"""

def test_google_credentials(credentials_file='credentials.json'):
    """Teste si le fichier de credentials existe et est valide."""
    import os
    
    if not os.path.exists(credentials_file):
        print(f"❌ Fichier credentials non trouvé: {credentials_file}")
        print("💡 Téléchargez le fichier JSON depuis Google Cloud Console")
        return False
    
    try:
        import json
        with open(credentials_file, 'r') as f:
            creds = json.load(f)
        
        required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email']
        missing_fields = [field for field in required_fields if field not in creds]
        
        if missing_fields:
            print(f"❌ Champs manquants dans credentials: {', '.join(missing_fields)}")
            return False
        
        print("✅ Fichier credentials valide")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lecture credentials: {e}")
        return False

def initialize_google_sheets(GoogleSheetsManager, GoogleSheetsInterface=None):
    """Initialise Google Sheets avec gestion d'erreur améliorée."""
    if not GoogleSheetsManager:
        print("⚠️  Google Sheets non disponible")
        return None
    
    # Vérifier le fichier credentials
    if not test_google_credentials():
        return None
    
    try:
        # Utiliser l'interface simplifiée si disponible
        if GoogleSheetsInterface:
            sheets_manager = GoogleSheetsInterface()
            print("✅ Interface Google Sheets prête")
        else:
            sheets_manager = GoogleSheetsManager()
            print("✅ Gestionnaire Google Sheets prêt")
        
        return sheets_manager
        
    except Exception as e:
        print(f"⚠️  Erreur initialisation Google Sheets: {e}")
        print("💡 Vérifiez:")
        print("   - Que le fichier credentials.json est valide")
        print("   - Que les APIs Google Sheets sont activées")
        print("   - Que les dépendances sont installées")
        return None

def configure_google_sheets(sheets_manager):
    """Configure Google Sheets avec validation améliorée."""
    if not sheets_manager:
        print("❌ Gestionnaire Google Sheets non disponible")
        return None
    
    print("\n📊 Configuration Google Sheets")
    print("=" * 50)
    print("💡 L'ID se trouve dans l'URL de votre Google Sheet:")
    print("   https://docs.google.com/spreadsheets/d/[ID_ICI]/edit")
    
    while True:
        print("\n" + "-" * 50)
        sheet_id = input("👉 ID de votre Google Sheet (ou 'skip' pour ignorer): ").strip()
        
        if sheet_id.lower() == 'skip':
            print("⏭️  Configuration Google Sheets ignorée")
            return None
        
        if not sheet_id:
            print("❌ Veuillez entrer un ID valide ou 'skip'")
            continue
        
        # Validation basique de l'ID
        if len(sheet_id) < 20:
            print("❌ L'ID semble trop court. Vérifiez qu'il s'agit bien de l'ID complet")
            continue
        
        try:
            # Configuration avec l'interface améliorée
            if hasattr(sheets_manager, 'setup_sheet'):
                success = sheets_manager.setup_sheet(sheet_id)
            else:
                # Méthode traditionnelle
                sheets_manager.set_spreadsheet(sheet_id)
                success = sheets_manager.create_trading_sheet()
            
            if success:
                print("✅ Configuration Google Sheets terminée!")
                
                # Afficher les infos de la sheet
                if hasattr(sheets_manager, 'print_status'):
                    sheets_manager.print_status()
                elif hasattr(sheets_manager, 'print_sheet_info'):
                    sheets_manager.print_sheet_info()
                
                return sheets_manager
            else:
                print("❌ Échec de la configuration")
                
        except Exception as e:
            print(f"❌ Erreur lors de la configuration: {e}")
            
            # Diagnostic plus détaillé
            if "404" in str(e):
                print("💡 La Google Sheet n'existe pas ou n'est pas accessible")
            elif "403" in str(e):
                print("💡 Permissions insuffisantes. Vérifiez que le compte de service a accès à la sheet")
            elif "400" in str(e):
                print("💡 ID invalide ou format incorrect")
        
        retry = input("🔄 Voulez-vous réessayer? (y/n): ").strip().lower()
        if retry != 'y':
            print("⏭️  Configuration Google Sheets ignorée")
            return None

def setup_google_sheets_integration(modules):
    """Configure l'intégration Google Sheets avec diagnostic complet."""
    print("\n" + "=" * 50)
    print("📊 INTÉGRATION GOOGLE SHEETS")
    print("=" * 50)
    
    if not modules['google_sheets_available']:
        print("❌ Google Sheets non disponible")
        print("💡 Pour l'activer, installez les dépendances:")
        print("   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        return None
    
    # Récupérer les classes disponibles
    GoogleSheetsManager = modules.get('GoogleSheetsManager')
    GoogleSheetsInterface = modules.get('GoogleSheetsInterface')
    
    # Initialiser le gestionnaire
    sheets_manager = initialize_google_sheets(GoogleSheetsManager, GoogleSheetsInterface)
    
    if sheets_manager:
        # Configurer si souhaité
        configured_sheets = configure_google_sheets(sheets_manager)
        
        if configured_sheets:
            print("\n✅ Google Sheets configuré et prêt à utiliser")
            print("💾 Vos analyses seront automatiquement sauvegardées")
            return configured_sheets
        else:
            print("\n📝 Fonctionnement sans sauvegarde Google Sheets")
            return None
    else:
        print("\n📝 Fonctionnement sans Google Sheets")
        return None

def create_sample_sheet_guide():
    """Affiche un guide pour créer une Google Sheet."""
    print("\n📖 GUIDE: Créer une Google Sheet pour le Trading Agent")
    print("=" * 60)
    print("1. Allez sur https://sheets.google.com")
    print("2. Créez une nouvelle feuille de calcul")
    print("3. Donnez-lui un nom (ex: 'Trading Analysis')")
    print("4. Copiez l'ID depuis l'URL")
    print("5. Partagez la sheet avec votre compte de service")
    print("6. Utilisez cet ID dans la configuration")
    print("=" * 60)
