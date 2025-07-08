import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'stocks'))

from stocks.portfolio import GAFAM
from stocks.get_data import get_stock_data
from .calculate_signals import calculate_signals

def analyze_quick(sheets_manager=None):
    print("🚀 ANALYSE RAPIDE - GAFAM")
    print("=" * 80)
    
    results = []
    
    for symbol, name in GAFAM.items():
        print(f"📊 Analyse de {symbol}...")
        
        data = get_stock_data(symbol)
        analysis = calculate_signals(data)
        
        if analysis: 
            # Calcul de la variation en pourcentage
            change_1d = 0
            if len(data) > 1:
                change_1d = ((analysis['price'] - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100
            
            result = {
                'Symbol': symbol,
                'Name': name,
                'Price': analysis['price'],
                'Decision': analysis['decision'],
                'Signals': f"{analysis['signal_count']}/3",
                'Change': change_1d
            }
            results.append(result)
            
            # Send to Google Sheets if available
            if sheets_manager:
                try:
                    analysis_data = {
                        'company': name,
                        'price': f"{analysis['price']:.2f}",
                        'rsi': 'N/A',
                        'macd': 'N/A',
                        'signal': ', '.join(analysis['signals']),
                        'recommendation': analysis['decision'],
                        'volume': f"{data['Volume'].iloc[-1]:.0f}" if len(data) > 0 else 'N/A',
                        'change_percent': f"{change_1d:.2f}%"
                    }
                    sheets_manager.append_analysis(symbol, analysis_data, analysis_type="Quick")
                except Exception as e:
                    print(f"⚠️  Erreur Google Sheets pour {symbol}: {e}")
    
    # Affichage des résultats
    print("\n📈 RÉSULTATS:")
    print("-" * 80)
    print(f"{'Symbol':<6} | {'Name':<20} | {'Price':<8} | {'Change':<8} | {'Decision':<15} | {'Signals'}")
    print("-" * 80)

    for result in results:
        change_color = "🟢" if result['Change'] > 0 else "🔴" if result['Change'] < 0 else "⚪"
        decision_icon = "🟢" if "ACHETER" in result['Decision'] else "🔴" if "VENDRE" in result['Decision'] else "🟡"
        
        print(f"{result['Symbol']:<6} | {result['Name']:<20} | ${result['Price']:<7.2f} | "
              f"{change_color}{result['Change']:+5.1f}% | {decision_icon}{result['Decision']:<14} | {result['Signals']}")
    
    # Résumé
    buy_count = sum(1 for r in results if "ACHETER" in r['Decision'])
    sell_count = sum(1 for r in results if "VENDRE" in r['Decision'])
    wait_count = sum(1 for r in results if "ATTENDRE" in r['Decision'])
    avg_change = sum(r['Change'] for r in results) / len(results) if results else 0
    
    print(f"\n📊 RÉSUMÉ:")
    print(f"🟢 À acheter: {buy_count}")
    print(f"🔴 À vendre: {sell_count}")
    print(f"🟡 À surveiller: {wait_count}")
    print(f"📈 Variation moyenne: {avg_change:+.2f}%")
    
    if sheets_manager:
        print(f"✅ Toutes les analyses sauvegardées dans Google Sheets")