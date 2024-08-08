from flask import Flask, request, render_template
from datetime import datetime
from data import StockAnalyzer
import json

app = Flask(__name__) 


@app.route("/") 
def home(): 		
    return render_template("index.html")

@app.route('/data')
def data():
    ticker = request.args.get('symbol')
    print(ticker)
    start_date = request.args.get('start-date')
    end_date = request.args.get('end-date')
    interval = request.args.get('interval')
    if start_date is not None and end_date is not None:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    stock = StockAnalyzer(ticker, start_date, end_date, interval)
    nifty = StockAnalyzer('^NSEI', start_date, end_date, interval)

    print(stock.is_data_available())

    if stock.is_data_available():
        stock.download_data()
        nifty.download_data()
        missing_stock_data = None
        if stock.has_missing_data():
            missing_stock_data = stock.handle_missing_data()
        if nifty.has_missing_data():
            nifty.handle_missing_data()
        stock_stats = stock.get_statistial_measure()
        stock.add_cummulative_return()
        nifty.add_cummulative_return()

        columns = stock_stats.columns
        rows = stock_stats.values.tolist()

        if stock.data.columns[0] == 'Date':
            labels = stock.data[stock.data.columns[0]].apply(lambda x: x.strftime('%Y-%m-%d'))
            labels = labels.tolist()
        else:
            labels = stock.data[stock.data.columns[0]].apply(lambda x: x.strftime('%Y-%m-%d %H:%M'))
            labels = labels.tolist()

        data = {
            'labels': labels,
            'stock_cummulative_return': list(stock.data['Cummulative Return']),
            'nifty_cummulative_return': list(nifty.data['Cummulative Return'])
        }

        json_data = json.dumps(data)

        return render_template('data.html', columns=columns, rows=rows, missing_stock_data=missing_stock_data, stock_data=stock.data.round(2), json_data=json_data)   

    return render_template('error.html')    
        

if __name__ == '__main__': 
    app.run(debug=True) 
