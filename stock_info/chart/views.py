from .alpha_api import get_company_overview, get_news, get_time_series_daily
from chart import app
from flask import render_template, jsonify, make_response, flash

@app.route('/')
def index():
    return render_template("index.html", page_data={"title": "Duke Blue Pay: Home"})

@app.route('/stock/')
@app.route('/stock/<symbol>')
def show_stock_info(symbol=None):
    if symbol:
        page_data = {"title": "Duke Blue Pay: " + symbol, "inputValue": symbol}
        try:
            stock_data = get_company_overview(symbol)
            news_articles = get_news(symbol)
            # Extracting time series data
            time_series_data = get_time_series_daily(symbol)
            if 'Time Series (Daily)' in time_series_data:
                daily_data = time_series_data['Time Series (Daily)']
                dates = sorted(daily_data.keys(), reverse=True)
                most_recent_date = dates[0]
                previous_date = dates[1] if len(dates) > 1 else None
                most_recent_close = daily_data[most_recent_date]['4. close'] if most_recent_date else None
                previous_close = daily_data[previous_date]['4. close'] if previous_date else None
                most_recent_volume = daily_data[most_recent_date]['6. volume'] if most_recent_date else None
                most_recent_open = daily_data[most_recent_date]['1. open'] if most_recent_date else None
                # Add these to stock_data dictionary 
                stock_data['most_recent_close'] = most_recent_close
                stock_data['previous_close'] = previous_close
                stock_data['most_recent_volume'] = most_recent_volume
                stock_data['most_recent_open'] = most_recent_open
            return render_template("stock.html", page_data=page_data, stock_data=stock_data, symbol=symbol, news_articles=news_articles)
    
        except Exception as e:
            flash(f'Error fetching live stock data for {symbol}: {str(e)}', 'error')
        
        
    else:
        page_data = {"title": "Duke Blue Pay: Stock Information", "inputValue": ""}
    return render_template("stock.html", page_data=page_data, stock_data=None, news_articles=[])


@app.route('/stock/pricing/<symbol>')
def retrieve_stock_prices(symbol = None):
    if not symbol:
        return make_response(jsonify({'error': 'Symbol is required'}), 400)

    time_series_data = get_time_series_daily(symbol)
    # Check for an error message in the response
    if 'Error Message' in time_series_data:
        app.logger.error(f"API error: {time_series_data['Error Message']}")
        return make_response(jsonify({'error': 'Failed to fetch stock data', 'details': time_series_data['Error Message']}), 404)

    # Check if the 'Time Series (Daily)' data is in the response
    if 'Time Series (Daily)' in time_series_data:
        daily_data = time_series_data['Time Series (Daily)']
        dates = []
        adj_close_prices = []
        # Iterate over the sorted keys (dates) to maintain chronological order
        for date in sorted(daily_data.keys()):
            dates.append(date)
            adj_close_prices.append(daily_data[date]['4. close'])
        
        result = {
            "symbol": symbol.upper(),
            "dates": dates,
            "adjClosePrices": adj_close_prices
        }
        return jsonify(result)
    else:
        app.logger.error("Time Series (Daily) data not found in the API response.")
        return make_response(jsonify({'error': 'Time Series (Daily) data not found'}), 404)


