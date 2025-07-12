# 📊 Trading Agent Simple - PERSO

Un outil Python simple pour analyser les actions GAFAM (Apple, Google, Microsoft, Amazon, Meta).

## 🎯 Fonctionnalités

- **Analyse rapide** : Vue d'ensemble des 5 actions GAFAM
- **Analyse détaillée** : Analyse approfondie d'une action spécifique

## 📈 Signaux de Trading

Le système utilise 3 signaux simples :

1. **Prix > MA20** : Le prix est au-dessus de la moyenne mobile 20 jours
2. **Prix > MA50** : Le prix est au-dessus de la moyenne mobile 50 jours  
3. **MA20 > MA50** : La moyenne courte est au-dessus de la moyenne longue

### Décisions :
- **🟢 ACHETER** : 3/3 signaux positifs
- **🔴 VENDRE** : 0/3 signaux positifs
- **🟡 ATTENDRE** : 1/3 ou 2/3 signaux positifs

## 🔧 Installation

```bash
# Installer les dépendances
pip install -r requirements_simple.txt
# Ou manuellement
pip install yfinance pandas
```

## 🚀 Utilisation

```bash
python main.py
```

Le programme vous propose deux options :

1. **Analyse rapide** : Affiche un résumé des 5 actions GAFAM
2. **Analyse détaillée** : Analyse complète d'une action spécifique

## 📊 Exemple d'utilisation

```
🎯 TRADING AGENT SIMPLE
============================================================
📊 Portefeuille: GAFAM (5 actions)
⏰ 2024-01-15 14:30:00
============================================================

Que voulez-vous faire ?
1. 🚀 Analyse rapide (toutes les actions)
2. 🔍 Analyse détaillée (une action)
3. ❌ Quitter

👉 Votre choix (1-3): 1

🚀 ANALYSE RAPIDE - GAFAM
============================================================
📊 Analyse de AAPL...
📊 Analyse de GOOGL...
📊 Analyse de MSFT...
📊 Analyse de AMZN...
📊 Analyse de META...

📈 RÉSULTATS:
------------------------------------------------------------
AAPL  | Apple                | $175.30 | 🟢 ACHETER  | 3/3
GOOGL | Google (Alphabet)    | $142.50 | 🟡 ATTENDRE | 2/3
MSFT  | Microsoft            | $398.20 | 🟢 ACHETER  | 3/3
AMZN  | Amazon               | $155.90 | 🔴 VENDRE   | 0/3
META  | Meta (Facebook)      | $350.80 | 🟡 ATTENDRE | 1/3

📊 RÉSUMÉ:
🟢 À acheter: 2
🔴 À vendre: 1
🟡 À surveiller: 2
```

## 🔮 Prochaines étapes

Ce code simple peut être étendu avec :

- Plus d'actions et de secteurs
- Indicateurs techniques supplémentaires
- Alertes par email/SMS
- Interface graphique
- Sauvegarde des analyses
- Backtesting

## 📝 Disclaimer

- Les données proviennent de Yahoo Finance
- Les analyses sont basées sur les moyennes mobiles
- Ce n'est pas un conseil financier !
- Toujours faire ses propres recherches avant d'investir
