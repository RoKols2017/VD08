from flask import Flask, render_template
import requests

app = Flask(__name__)
API_KEY = 'demo'

def get_exchange_rate(from_currency, to_currency):
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={API_KEY}"
    try:
        r = requests.get(url)
        data = r.json()
        rate_info = data["Realtime Currency Exchange Rate"]
        rate = rate_info["5. Exchange Rate"]
        time = rate_info["6. Last Refreshed"]
        return float(rate), time
    except Exception:
        return None, None

def get_ibm_stock_price():
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={API_KEY}'
    try:
        r = requests.get(url)
        data = r.json()
        time_series = data.get("Time Series (5min)", {})
        if not time_series:
            raise ValueError("Нет данных")
        latest_time = sorted(time_series.keys())[-1]
        latest_data = time_series[latest_time]
        price = latest_data["1. open"]
        return float(price), latest_time
    except Exception:
        return None, None

@app.route('/')
def index():
    gold_price, gold_time = get_exchange_rate("XAU", "USD")
    eur_usd, eur_time = get_exchange_rate("EUR", "USD")
    ibm_price, ibm_time = get_ibm_stock_price()

    brent_price = "Недоступно в demo API"
    brent_time = "-"

    return render_template("index.html",
                           gold_price=gold_price,
                           gold_time=gold_time,
                           eur_usd=eur_usd,
                           eur_time=eur_time,
                           brent_price=brent_price,
                           brent_time=brent_time,
                           ibm_price=ibm_price,
                           ibm_time=ibm_time)

if __name__ == '__main__':
    app.run(debug=True)
