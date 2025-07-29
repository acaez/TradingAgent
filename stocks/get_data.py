import yfinance as yf
from datetime import datetime, timedelta

def get_stock_data(symbol, days=60):
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days + 20)
        
        stock = yf.Ticker(symbol)
        data = stock.history(start=start_date, end=end_date)
        
        if data.empty:
            return None
            
        return data.tail(days)
    except Exception as e:
        print(f"❌ Erreur pour {symbol}: {e}")
        return None