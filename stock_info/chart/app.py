from flask import Flask, render_template, request, url_for, flash, redirect
import requests
from .config import ALPHA_VANTAGE_API_KEY

app = Flask(__name__)
app.secret_key = 'XHDWCYWJPUFFPBQK'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        symbol = request.form.get('symbol')
        if not symbol:
            flash('Stock symbol is required!', 'error')
            return redirect(url_for('index'))
        return redirect(url_for('stock_info', symbol=symbol))
    return render_template('index.html')

@app.route('/stock/<symbol>')
def stock_info(symbol):
    data = {}
    try:
        overview_url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
        response = requests.get(overview_url)
        if response.status_code == 200:
            data = response.json()
            if not data:
                flash('No data found for the symbol.', 'error')
                return redirect(url_for('index'))
        else:
            flash('Failed to fetch data from Alpha Vantage.', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash(str(e), 'error')
        return redirect(url_for('index'))
    return render_template('stock.html', symbol=symbol, page_data=data)

if __name__ == '__main__':
    app.run(debug=True)
