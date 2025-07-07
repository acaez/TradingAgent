"""
Analyse rapide de toutes les actions GAFAM
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'stocks'))

from stocks.portfolio import GAFAM
from stocks.get_data import get_stock_data
from .calculate_signals import calculate_signals

def analyze_quick():
    """
    Analyse rapide de toutes les actions GAFAM
    """
    print("🚀 ANALYSE RAPIDE - GAFAM")
    print("=" * 60)
    
    results = []
    
    for symbol, name in GAFAM.items():
        print(f"📊 Analyse de {symbol}...")
        
        data = get_stock_data(symbol)
        analysis = calculate_signals(data)
        
        if analysis:
            results.append({
                'Symbol': symbol,
                'Name': name,
                'Price': analysis['price'],
                'Decision': analysis['decision'],
                'Signals': f"{analysis['signal_count']}/3"
            })
    
    # Affichage des résultats
    print("\n📈 RÉSULTATS:")
    print("-" * 60)
    for result in results:
        print(f"{result['Symbol']:5} | {result['Name']:20} | ${result['Price']:7.2f} | {result['Decision']} | {result['Signals']}")
    
    # Résumé
    buy_count = sum(1 for r in results if "ACHETER" in r['Decision'])
    sell_count = sum(1 for r in results if "VENDRE" in r['Decision'])
    wait_count = sum(1 for r in results if "ATTENDRE" in r['Decision'])
    
    print(f"\n📊 RÉSUMÉ:")
    print(f"🟢 À acheter: {buy_count}")
    print(f"🔴 À vendre: {sell_count}")
    print(f"🟡 À surveiller: {wait_count}")