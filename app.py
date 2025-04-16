from flask import Flask, render_template
import requests

app = Flask(__name__)

API_KEY = 'demo'  # ⚠️ замените на свой ключ, если нужно
SYMBOL = 'IBM'
API_URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={SYMBOL}&interval=5min&apikey={API_KEY}'

@app.route('/')
def home():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        time_series = data.get("Time Series (5min)", {})
        if not time_series:
            raise ValueError("Нет данных о ценах")

        latest_timestamp = sorted(time_series.keys())[-1]
        latest_data = time_series[latest_timestamp]
        price = latest_data.get("1. open", "Неизвестно")

    except Exception as e:
        latest_timestamp = "Ошибка"
        price = "Невозможно получить цену"

    return render_template('index.html', symbol=SYMBOL, time=latest_timestamp, price=price)

if __name__ == '__main__':
    app.run(debug=True)
