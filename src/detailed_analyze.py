import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'stocks'))

from stocks.portfolio import GAFAM
from stocks.get_data import get_stock_data
from .calculate_signals import calculate_signals

def analyze_detailed(symbol):
    if symbol not in GAFAM:
        print(f"❌ '{symbol}' n'existe pas dans notre portefeuille")
        print("📋 Symboles disponibles:", ", ".join(GAFAM.keys()))
        return
    
    print(f"🔍 ANALYSE DÉTAILLÉE - {symbol}")
    print("=" * 60)
    print(f"🏢 Société: {GAFAM[symbol]}")
    print("=" * 60)
    
    print("📥 Récupération des données...")
    data = get_stock_data(symbol)
    
    if data is None:
        print("❌ Impossible de récupérer les données")
        return
    
    analysis = calculate_signals(data)
    if analysis is None:
        print("❌ Pas assez de données pour l'analyse")
        return
    
    print("\n💰 INFORMATIONS PRINCIPALES:")
    print("-" * 60)
    print(f"Prix actuel: ${analysis['price']:.2f}")
    print(f"Moyenne 20 jours: ${analysis['ma20']:.2f}")
    if analysis['ma50']:
        print(f"Moyenne 50 jours: ${analysis['ma50']:.2f}")
    
    print("\n🚦 SIGNAUX DE TRADING:")
    print("-" * 60)
    print(f"Décision: {analysis['decision']}")
    print(f"Signaux actifs: {analysis['signal_count']}/3")
    
    if analysis['signals']:
        print("✅ Signaux positifs:")
        for signal in analysis['signals']:
            print(f"   • {signal}")
    else:
        print("❌ Aucun signal positif")
    
    print("\n📊 INFORMATIONS SUPPLÉMENTAIRES:")
    print("-" * 60)
    
    last_30_days = data.tail(30)
    highest_price = last_30_days['High'].max()
    lowest_price = last_30_days['Low'].min()
    
    print(f"Prix le plus haut (30j): ${highest_price:.2f}")
    print(f"Prix le plus bas (30j): ${lowest_price:.2f}")
    
    performance = ((analysis['price'] - lowest_price) / lowest_price) * 100
    print(f"Performance depuis le plus bas: +{performance:.1f}%")
    
    distance_from_high = ((highest_price - analysis['price']) / analysis['price']) * 100
    print(f"Distance du plus haut: -{distance_from_high:.1f}%")
    
    avg_volume = data['Volume'].tail(10).mean()
    print(f"Volume moyen (10j): {avg_volume:,.0f}")
    
    print("\n💡 CONSEIL SIMPLE:")
    print("-" * 60)
    if analysis['signal_count'] == 3:
        print("🟢 Tous les signaux sont positifs - Bon moment pour acheter")
    elif analysis['signal_count'] == 2:
        print("🟡 Signaux mixtes - Attendre une confirmation")
    elif analysis['signal_count'] == 1:
        print("🟠 Peu de signaux positifs - Prudence recommandée")
    else:
        print("🔴 Aucun signal positif - Éviter d'acheter maintenant")
