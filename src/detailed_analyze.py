import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'stocks'))

from stocks.portfolio import PERSO
from stocks.get_data import get_stock_data
from .calculate_signals import calculate_signals

def analyze_detailed(symbol, sheets_manager=None):
    if symbol not in PERSO:
        print(f"❌ '{symbol}' n'existe pas dans notre portefeuille")
        print("📋 Symboles disponibles:", ", ".join(PERSO.keys()))
        return
    
    company_name = PERSO[symbol]
    
    print(f"🔍 ANALYSE DÉTAILLÉE - {symbol}")
    print("=" * 80)
    print(f"🏢 Société: {company_name}")
    print("=" * 80)
    
    print("📥 Récupération des données...")
    data = get_stock_data(symbol, days=252)
    
    if data is None:
        print("❌ Impossible de récupérer les données")
        return
    
    analysis = calculate_signals(data)
    if analysis is None:
        print("❌ Pas assez de données pour l'analyse")
        return

    current_price = analysis['price']
    decision = analysis['decision']
    signals = analysis['signals']
    signal_count = analysis['signal_count']
    
    print(f"💰 PRIX ACTUEL: ${current_price:.2f}")
    print(f"📊 VOLUME: {data['Volume'].iloc[-1]:,.0f}")
    
    high_52w = data['High'].rolling(window=252).max().iloc[-1]
    low_52w = data['Low'].rolling(window=252).min().iloc[-1]
    change_1d = ((current_price - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100
    change_5d = ((current_price - data['Close'].iloc[-6]) / data['Close'].iloc[-6]) * 100 if len(data) > 5 else 0
    
    print(f"📈 Plus haut 52 semaines: ${high_52w:.2f}")
    print(f"📉 Plus bas 52 semaines: ${low_52w:.2f}")
    print(f"🔄 Variation 1 jour: {change_1d:+.2f}%")
    print(f"🔄 Variation 5 jours: {change_5d:+.2f}%")
    
    print("\n🎯 SIGNAUX DE TRADING:")
    print("-" * 40)
    for i, signal in enumerate(signals, 1):
        print(f"  {i}. {signal}")
    
    print(f"\n📊 FORCE DU SIGNAL: {signal_count}/3")
    
    # Recommandation avec explication
    print(f"\n💡 RECOMMANDATION: {decision}")
    print("-" * 40)
    
    if "ACHETER" in decision:
        print("🟢 Les signaux techniques sont favorables à l'achat")
        print("   • Tendance haussière confirmée")
        print("   • Moment opportun pour entrer en position")
    elif "VENDRE" in decision:
        print("🔴 Les signaux techniques suggèrent la vente")
        print("   • Tendance baissière détectée")
        print("   • Risque de correction à court terme")
    else:
        print("🟡 Position d'attente recommandée")
        print("   • Signaux mixtes ou neutres")
        print("   • Surveiller l'évolution avant de prendre position")
    
    # Niveaux de support et résistance basiques
    recent_data = data.tail(20)
    support = recent_data['Low'].min()
    resistance = recent_data['High'].max()
    
    print(f"\n📊 NIVEAUX TECHNIQUES:")
    print(f"   🔻 Support: ${support:.2f}")
    print(f"   🔺 Résistance: ${resistance:.2f}")
    
    if sheets_manager:
        try:
            analysis_data = {
                'company': company_name,
                'price': f"{current_price:.2f}",
                'rsi': 'N/A',
                'macd': 'N/A',
                'signal': ', '.join(signals),
                'recommendation': decision,
                'volume': f"{data['Volume'].iloc[-1]:.0f}",
                'change_percent': f"{change_1d:.2f}%"
            }
            sheets_manager.append_analysis(symbol, analysis_data, analysis_type="Detailed")
            print(f"\n✅ Analyse sauvegardée dans Google Sheets")
        except Exception as e:
            print(f"\n⚠️  Erreur Google Sheets: {e}")
    
    print("\n" + "=" * 80)
