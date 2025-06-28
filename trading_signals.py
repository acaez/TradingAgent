import yfinance as yf
import pandas as pd

# Liste des actions à analyser
STOCKS = {
    'AAPL': 'Apple',
    'TSLA': 'Tesla', 
    'GOOGL': 'Google',
    'MSFT': 'Microsoft',
    'NVDA': 'NVIDIA',
    'AMZN': 'Amazon'
}

def download_stock_data(symbol, start_date="2024-01-01", end_date="2024-12-31"):
    """
    Télécharge les données boursières pour un symbole donné
    
    Args:
        symbol (str): Symbole boursier (ex: 'AAPL')
        start_date (str): Date de début (format 'YYYY-MM-DD')
        end_date (str): Date de fin (format 'YYYY-MM-DD')
    
    Returns:
        pandas.DataFrame: Données boursières ou None si erreur
    """
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date, progress=False)
        return stock_data
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement de {symbol}: {str(e)}")
        return None

def calculate_moving_averages(stock_data):
    """
    Calcule les moyennes mobiles MA20 et MA50
    
    Args:
        stock_data (pandas.DataFrame): Données boursières
    
    Returns:
        pandas.DataFrame: Données avec moyennes mobiles ajoutées
    """
    stock_data['MA20'] = stock_data['Close'].rolling(window=20).mean()
    stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()
    return stock_data

def analyze_signals(stock_data):
    """
    Analyse les signaux de trading basés sur les moyennes mobiles
    
    Args:
        stock_data (pandas.DataFrame): Données avec moyennes mobiles
    
    Returns:
        dict: Dictionnaire contenant l'analyse des signaux
    """
    # Récupération des valeurs actuelles (dernière ligne)
    current_price = stock_data['Close'].iloc[-1].item()
    current_ma20 = stock_data['MA20'].iloc[-1].item()
    current_ma50 = stock_data['MA50'].iloc[-1].item()
    
    # Calcul des conditions haussières
    above_ma20 = current_price > current_ma20
    above_ma50 = current_price > current_ma50
    ma20_above_ma50 = current_ma20 > current_ma50
    
    # Comptage des signaux haussiers
    bullish_count = sum([above_ma20, above_ma50, ma20_above_ma50])
    
    # Détermination du signal global
    if bullish_count == 3:
        signal = "🟢 STRONG BUY"
    elif bullish_count == 2:
        signal = "🟡 BUY"
    elif bullish_count == 1:
        signal = "🟡 NEUTRAL"
    else:
        signal = "🔴 SELL"
    
    return {
        'price': current_price,
        'ma20': current_ma20,
        'ma50': current_ma50,
        'above_ma20': above_ma20,
        'above_ma50': above_ma50,
        'ma20_above_ma50': ma20_above_ma50,
        'bullish_count': bullish_count,
        'signal': signal
    }

def analyze_single_stock(symbol, name, start_date="2024-01-01", end_date="2024-12-31"):
    """
    Analyse complète d'une action individuelle
    
    Args:
        symbol (str): Symbole boursier
        name (str): Nom de l'entreprise
        start_date (str): Date de début
        end_date (str): Date de fin
    
    Returns:
        dict: Résultats de l'analyse ou None si erreur
    """
    print(f"📊 Analyse de {name} ({symbol})...")
    
    # Téléchargement des données
    stock_data = download_stock_data(symbol, start_date, end_date)
    if stock_data is None:
        return None
    
    # Calcul des moyennes mobiles
    stock_data = calculate_moving_averages(stock_data)
    
    # Analyse des signaux
    signals = analyze_signals(stock_data)
    
    # Affichage des résultats
    print(f"Prix: ${signals['price']:.2f} | MA20: ${signals['ma20']:.2f} | MA50: ${signals['ma50']:.2f}")
    print(f"Signaux haussiers: {signals['bullish_count']}/3 | {signals['signal']}")
    
    # Préparation du résultat final
    result = {
        'Symbol': symbol,
        'Name': name,
        'Price': signals['price'],
        'MA20': signals['ma20'],
        'MA50': signals['ma50'],
        'Bullish_Signals': signals['bullish_count'],
        'Signal': signals['signal'],
        'Stock_Data': stock_data  # Ajout des données pour les graphiques
    }
    
    return result

def analyze_multiple_stocks(stocks=None, start_date="2024-01-01", end_date="2024-12-31"):
    """
    Analyse plusieurs actions et génère un rapport de synthèse
    
    Args:
        stocks (dict): Dictionnaire {symbole: nom} ou None pour utiliser STOCKS par défaut
        start_date (str): Date de début
        end_date (str): Date de fin
    
    Returns:
        pandas.DataFrame: DataFrame avec tous les résultats triés
    """
    if stocks is None:
        stocks = STOCKS
    
    print("🚀 Analyse Multi-Actions")
    print("=" * 50)
    
    results = []
    
    # Analyse de chaque action
    for symbol, name in stocks.items():
        result = analyze_single_stock(symbol, name, start_date, end_date)
        if result is not None:
            results.append(result)
    
    # Création du DataFrame et tri
    if results:
        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values('Bullish_Signals', ascending=False)
        
        # Affichage du tableau de synthèse
        display_summary_table(results_df)
        display_top_picks(results_df)
        
        return results_df
    else:
        print("❌ Aucune donnée analysée avec succès")
        return pd.DataFrame()

def display_summary_table(results_df):
    """
    Affiche le tableau de synthèse des résultats
    
    Args:
        results_df (pandas.DataFrame): DataFrame avec les résultats
    """
    print("\n" + "=" * 80)
    print("📈 TABLEAU DE SYNTHÈSE DES SIGNAUX")
    print("=" * 80)
    
    print(f"{'Action':<10} {'Nom':<12} {'Prix':<10} {'MA20':<10} {'MA50':<10} {'Signaux':<8} {'Signal'}")
    print("-" * 80)
    
    for _, row in results_df.iterrows():
        print(f"{row['Symbol']:<10} {row['Name']:<12} ${row['Price']:<9.2f} ${row['MA20']:<9.2f} ${row['MA50']:<9.2f} {row['Bullish_Signals']}/3{'':<4} {row['Signal']}")

def display_top_picks(results_df):
    """
    Affiche les meilleures et pires actions
    
    Args:
        results_df (pandas.DataFrame): DataFrame avec les résultats
    """
    print("\n🏆 MEILLEURES OPPORTUNITÉS:")
    strong_buys = results_df[results_df['Bullish_Signals'] == 3]
    if not strong_buys.empty:
        print("🟢 Signaux STRONG BUY:")
        for _, row in strong_buys.iterrows():
            print(f"   • {row['Name']} ({row['Symbol']}) - ${row['Price']:.2f}")
    else:
        print("Aucun signal STRONG BUY trouvé")
    
    print("\n⚠️  ACTIONS LES PLUS FAIBLES:")
    weak_stocks = results_df[results_df['Bullish_Signals'] <= 1]
    if not weak_stocks.empty:
        for _, row in weak_stocks.iterrows():
            print(f"   • {row['Name']} ({row['Symbol']}) - {row['Signal']}")
    else:
        print("Toutes les actions montrent des signaux corrects !")

# Fonction principale pour tester le module
if __name__ == "__main__":
    # Analyse complète avec affichage des résultats
    results = analyze_multiple_stocks()
    
    print("\n✅ Analyse des signaux terminée!")
    print("💡 Concentrez-vous sur les actions avec 3/3 signaux haussiers!")