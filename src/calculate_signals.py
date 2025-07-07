"""
Calcul des signaux de trading
"""

import pandas as pd

def calculate_signals(data):
    """
    Calcule les signaux de trading
    
    Args:
        data (pandas.DataFrame): Données de l'action
    
    Returns:
        dict: Signaux et indicateurs
    """
    if data is None or len(data) < 20:
        return None
    
    # Calcul des moyennes mobiles
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()
    
    # Dernières valeurs
    latest = data.iloc[-1]
    price = latest['Close']
    ma20 = latest['MA20']
    ma50 = latest['MA50']
    
    # Vérification des valeurs valides - seulement MA20 requis
    if pd.isna(ma20):
        return None
    
    # Calcul des signaux
    signals = []
    
    # Signal 1: Prix > MA20
    if price > ma20:
        signals.append("Prix > MA20")
    
    # Signal 2: Prix > MA50 (seulement si MA50 existe)
    if not pd.isna(ma50) and price > ma50:
        signals.append("Prix > MA50")
    
    # Signal 3: MA20 > MA50 (seulement si MA50 existe)
    if not pd.isna(ma50) and ma20 > ma50:
        signals.append("MA20 > MA50")
    
    # Décision finale
    signal_count = len(signals)
    if signal_count == 3:
        decision = "🟢 ACHETER"
    elif signal_count == 0:
        decision = "🔴 VENDRE"
    else:
        decision = "🟡 ATTENDRE"
    
    return {
        'price': price,
        'ma20': ma20,
        'ma50': ma50 if not pd.isna(ma50) else None,
        'signals': signals,
        'signal_count': signal_count,
        'decision': decision
    }
