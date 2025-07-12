"""
Calcul des signaux de trading
"""

import pandas as pd

def calculate_signals(data):

    if data is None or len(data) < 20:
        return None
    
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()
    latest = data.iloc[-1]
    price = latest['Close']
    ma20 = latest['MA20']
    ma50 = latest['MA50']
    if pd.isna(ma20):
        return None
    signals = []
    if price > ma20:
        signals.append("Prix > MA20")
    if not pd.isna(ma50) and price > ma50:
        signals.append("Prix > MA50")
    if not pd.isna(ma50) and ma20 > ma50:
        signals.append("MA20 > MA50")
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
