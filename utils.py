"""
Fonctions utilitaires pour l'analyse boursière
==============================================

Ce module contient des fonctions d'aide pour gérer les erreurs,
valider les données et formater les sorties.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings

def suppress_warnings():
    """Supprime les warnings non critiques pour une sortie plus propre"""
    warnings.filterwarnings('ignore', category=FutureWarning, module='yfinance')
    warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')

def validate_date_format(date_string):
    """
    Valide le format d'une date
    
    Args:
        date_string (str): Date au format 'YYYY-MM-DD'
    
    Returns:
        bool: True si valide, False sinon
    """
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def get_trading_days_count(start_date, end_date):
    """
    Estime le nombre de jours de trading entre deux dates
    
    Args:
        start_date (str): Date de début
        end_date (str): Date de fin
    
    Returns:
        int: Nombre approximatif de jours de trading
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        total_days = (end - start).days
        # Approximation: ~250 jours de trading par an (sur 365)
        return int(total_days * (250/365))
    except:
        return 250  # Valeur par défaut

def clean_stock_data(stock_data):
    """
    Nettoie les données boursières des valeurs manquantes et aberrantes
    
    Args:
        stock_data (pandas.DataFrame): Données boursières brutes
    
    Returns:
        pandas.DataFrame: Données nettoyées
    """
    if stock_data is None or stock_data.empty:
        return None
    
    # Suppression des lignes avec des valeurs manquantes dans les prix
    stock_data = stock_data.dropna(subset=['Open', 'High', 'Low', 'Close'])
    
    # Vérification des prix cohérents (pas de prix négatifs)
    stock_data = stock_data[stock_data['Close'] > 0]
    
    # Suppression des valeurs aberrantes (variation > 50% en une journée)
    daily_change = stock_data['Close'].pct_change().abs()
    stock_data = stock_data[daily_change < 0.5]
    
    return stock_data

def safe_calculate_indicators(stock_data, ma_short=20, ma_long=50):
    """
    Calcule les indicateurs techniques de façon sécurisée
    
    Args:
        stock_data (pandas.DataFrame): Données boursières
        ma_short (int): Période courte pour moyenne mobile
        ma_long (int): Période longue pour moyenne mobile
    
    Returns:
        pandas.DataFrame: Données avec indicateurs ajoutés
    """
    if stock_data is None or len(stock_data) < ma_long:
        print(f"⚠️  Pas assez de données pour calculer MA{ma_long}")
        return stock_data
    
    try:
        # Calcul des moyennes mobiles
        stock_data[f'MA{ma_short}'] = stock_data['Close'].rolling(window=ma_short, min_periods=ma_short).mean()
        stock_data[f'MA{ma_long}'] = stock_data['Close'].rolling(window=ma_long, min_periods=ma_long).mean()
        
        # Calcul du RSI (Relative Strength Index)
        delta = stock_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        stock_data['RSI'] = 100 - (100 / (1 + rs))
        
        # Calcul de la volatilité (écart-type sur 20 jours)
        stock_data['Volatility'] = stock_data['Close'].rolling(window=20).std()
        
        return stock_data
    
    except Exception as e:
        print(f"❌ Erreur lors du calcul des indicateurs: {str(e)}")
        return stock_data

def format_price(price):
    """
    Formate un prix pour l'affichage
    
    Args:
        price (float): Prix à formater
    
    Returns:
        str: Prix formaté
    """
    if pd.isna(price):
        return "N/A"
    return f"${price:.2f}"

def format_percentage(value):
    """
    Formate un pourcentage pour l'affichage
    
    Args:
        value (float): Valeur à formater en pourcentage
    
    Returns:
        str: Pourcentage formaté
    """
    if pd.isna(value):
        return "N/A"
    return f"{value:.2f}%"

def get_signal_emoji(bullish_count):
    """
    Retourne l'emoji correspondant au nombre de signaux haussiers
    
    Args:
        bullish_count (int): Nombre de signaux haussiers (0-3)
    
    Returns:
        str: Emoji correspondant
    """
    emojis = {
        0: "🔴",
        1: "🟡", 
        2: "🟠",
        3: "🟢"
    }
    return emojis.get(bullish_count, "❓")

def create_summary_stats(results_df):
    """
    Crée des statistiques de synthèse sur les résultats d'analyse
    
    Args:
        results_df (pandas.DataFrame): DataFrame avec les résultats
    
    Returns:
        dict: Dictionnaire avec les statistiques
    """
    if results_df.empty:
        return {}
    
    stats = {
        'total_stocks': len(results_df),
        'strong_buy_count': len(results_df[results_df['Bullish_Signals'] == 3]),
        'buy_count': len(results_df[results_df['Bullish_Signals'] == 2]),
        'neutral_count': len(results_df[results_df['Bullish_Signals'] == 1]),
        'sell_count': len(results_df[results_df['Bullish_Signals'] == 0]),
        'avg_price': results_df['Price'].mean(),
        'highest_price': results_df['Price'].max(),
        'lowest_price': results_df['Price'].min(),
        'avg_signals': results_df['Bullish_Signals'].mean()
    }
    
    return stats

def print_summary_stats(stats):
    """
    Affiche les statistiques de synthèse de façon formatée
    
    Args:
        stats (dict): Dictionnaire des statistiques
    """
    if not stats:
        print("❌ Aucune statistique disponible")
        return
    
    print("\n📊 STATISTIQUES DE SYNTHÈSE")
    print("=" * 40)
    print(f"📈 Total d'actions analysées: {stats['total_stocks']}")
    print(f"🟢 STRONG BUY: {stats['strong_buy_count']} ({stats['strong_buy_count']/stats['total_stocks']*100:.1f}%)")
    print(f"🟠 BUY: {stats['buy_count']} ({stats['buy_count']/stats['total_stocks']*100:.1f}%)")
    print(f"🟡 NEUTRAL: {stats['neutral_count']} ({stats['neutral_count']/stats['total_stocks']*100:.1f}%)")
    print(f"🔴 SELL: {stats['sell_count']} ({stats['sell_count']/stats['total_stocks']*100:.1f}%)")
    print(f"💰 Prix moyen: {format_price(stats['avg_price'])}")
    print(f"📊 Signaux moyens: {stats['avg_signals']:.1f}/3")

def export_results_to_csv(results_df, filename=None):
    """
    Exporte les résultats vers un fichier CSV
    
    Args:
        results_df (pandas.DataFrame): DataFrame à exporter
        filename (str): Nom du fichier (optionnel)
    
    Returns:
        str: Nom du fichier créé
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analyse_boursiere_{timestamp}.csv"
    
    try:
        # Préparation des données pour l'export (suppression de la colonne Stock_Data si présente)
        export_df = results_df.copy()
        if 'Stock_Data' in export_df.columns:
            export_df = export_df.drop('Stock_Data', axis=1)
        
        export_df.to_csv(filename, index=False, encoding='utf-8')
        print(f"✅ Résultats exportés vers: {filename}")
        return filename
    
    except Exception as e:
        print(f"❌ Erreur lors de l'export: {str(e)}")
        return None

def validate_stock_symbol(symbol):
    """
    Valide un symbole boursier
    
    Args:
        symbol (str): Symbole à valider
    
    Returns:
        bool: True si valide, False sinon
    """
    if not symbol or not isinstance(symbol, str):
        return False
    
    # Nettoyage du symbole
    symbol = symbol.strip().upper()
    
    # Vérifications basiques
    if len(symbol) < 1 or len(symbol) > 5:
        return False
    
    # Caractères autorisés (lettres uniquement pour simplifier)
    if not symbol.isalpha():
        return False
    
    return True

def get_market_session_info():
    """
    Retourne des informations sur la session de marché actuelle
    
    Returns:
        dict: Informations sur la session
    """
    now = datetime.now()
    
    # Heures de marché US (approximatif)
    market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
    
    is_weekend = now.weekday() >= 5  # Samedi=5, Dimanche=6
    is_market_hours = market_open <= now <= market_close and not is_weekend
    
    return {
        'current_time': now.strftime("%Y-%m-%d %H:%M:%S"),
        'is_market_hours': is_market_hours,
        'is_weekend': is_weekend,
        'next_open': market_open.strftime("%H:%M") if now < market_open else "09:30 (demain)",
        'next_close': market_close.strftime("%H:%M") if now < market_close else "16:00 (demain)"
    }

# Fonction d'initialisation du module
def initialize_utils():
    """Initialise le module utilitaires"""
    suppress_warnings()
    print("🔧 Module utilitaires initialisé")

if __name__ == "__main__":
    # Test des fonctions utilitaires
    initialize_utils()
    
    # Test des validations
    print(f"Date valide (2024-01-01): {validate_date_format('2024-01-01')}")
    print(f"Date invalide: {validate_date_format('2024-13-45')}")
    print(f"Symbole valide (AAPL): {validate_stock_symbol('AAPL')}")
    print(f"Symbole invalide: {validate_stock_symbol('123ABC')}")
    
    # Informations de session
    session_info = get_market_session_info()
    print(f"Session actuelle: {session_info}")