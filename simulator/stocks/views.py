from django.shortcuts import render, redirect
from .models import Portfolio, Stock, Transaction, Watchlist
from .forms import PortolioForm, StockForm, TransactionForm, WatchlistForm
from datetime import datetime


def addPortfolio(request):
    portfolios = Portfolio.objects.filter(user=request.user)

    if not portfolios:
        p = Portfolio.objects.create(user=request.user)
        p.save()

    return redirect('portfolio')


def portfolio(request):
    import yfinance as yf

    portfolios = Portfolio.objects.filter(user=request.user)
    if not portfolios:
       return redirect('addPortfolio')

    if request.method == 'POST':
        buy = request.POST['buy']
        shares = request.POST['numberOfShares']
        get_ticker = request.POST['ticker']
        ticker = yf.Ticker(get_ticker)
        api = ticker.info

        #check if stock exists, if it does just change its fields
        s = Stock.objects.create(name=api.get('longName'),
                                 ticker=ticker,
                                 stocksOwned=shares,
                                 portfolio=request.user.portfolio)
        s.save()
        # s = Stock(name="Apple", ticker="aapl", stocksOwned=2, priceBought=21.2, portfolio=user.portfolio)

        portfolio = request.user.portfolio

        if buy == "buy":
            buybool = True
            portfolio.cash = portfolio.cash - float(shares)*api.get('currentPrice')
            portfolio.cashInvested = portfolio.cashInvested + float(shares) * api.get('currentPrice')
            portfolio.save()
        else:
            buybool = False
            portfolio.cash = portfolio.cash + float(shares) * api.get('currentPrice')
            portfolio.cashInvested = portfolio.cashInvested - float(shares) * api.get('currentPrice')
            portfolio.save()

        t = Transaction.objects.create(stockName=api.get('longName'),
                                       bought=buybool,
                                       numberOfStocks=shares,
                                       stockPrice = api.get('currentPrice'),
                                       date=datetime.today(),
                                       portfolio=request.user.portfolio)
        t.save()

    stocks = Stock.objects.filter(portfolio=request.user.portfolio)

    cash = round(request.user.portfolio.cash, 2)
    cashInvested = round(request.user.portfolio.cashInvested, 2)

    return render(request, 'portfolio.html', {'portfolio': request.user.portfolio, 'cash': cash, 'cashInvested': cashInvested, 'stocks': stocks})


def stock_info(request):
    import yfinance as yf

    if request.method == "POST":
        get_ticker = request.POST['ticker']

        ticker = yf.Ticker(get_ticker)
        api = ticker.info

        if api.get("currentPrice") is None:
            api = "Error"

    # disable the Sell button if the user doesn't own stocks for that company
    #try the AllStocks model
    #find the stocks that belong to the portfolio and then find
    # if the user owns stocks from that company
        p = Stock.objects.filter(portfolio=request.user.portfolio)
        s = p.filter(ticker=ticker)

    return render(request, 'stock_info.html', {'api': api, 'stockOwned': s})


def buy(request):
    import yfinance as yf

    if request.method == 'POST':
        get_ticker = request.POST['ticker']
        ticker = yf.Ticker(get_ticker)
        api = ticker.info

    # also pass the portfolio available cash in order to check if the purchase is possible
    cash = request.user.portfolio.cash

    return render(request, 'buy.html', {'api': api, 'cash': cash})


def sell(request):
    import yfinance as yf

    if request.method == 'POST':
        get_ticker = request.POST['ticker']
        ticker = yf.Ticker(get_ticker)
        api = ticker.info

    # extract the number of stocks from AllStocks

    # also pass the portfolio available cash in order to check if the purchase is possible
    cash = request.user.portfolio.cash

    return render(request, 'sell.html', {'api': api, 'cash': cash})


def watchlist(request):
    import yfinance as yf
    tickers = []

    if request.method == "POST":
        #should check if the stock already exists SHOULD NOT ADD THE SAME STOCK TWICE
        pred_ticker = Watchlist.objects.all().values('ticker')
        for pred in pred_ticker:
            if pred['ticker'].lower() == request.POST["ticker"].lower():
                return redirect('watchlist')

        w = Watchlist.objects.create(ticker=request.POST["ticker"], portfolio=request.user.portfolio)

        w.save()
        return redirect('watchlist')
    else:
        allwatchstocks = Watchlist.objects.all()
        watchstocks = []
        watchItems = []

        for w in allwatchstocks:
            if w.portfolio == request.user.portfolio:
                watchstocks.append(w.ticker)
                watchItems.append({'id': w.id, 'ticker': w.ticker})

        for stock in watchstocks:
            tick = yf.Ticker(str(stock))
            api = tick.info

            # if api.get("currentPrice") is None:
            #     api = "Error"
            # else:
            tickers.append(api)

        # watchItems = Watchlist.objects.all().values()
    #      [{'id': 1, 'ticker': 'aapl', 'portfolio_id': 1}, {'id': 2, 'ticker': 'goog', 'portfolio_id': 1}]>

    return render(request, 'watchlist.html', {'tickers': tickers, 'watchItems': watchItems})


def delete(request, stock_id):
    item = Watchlist.objects.get(pk=stock_id)
    item.delete()
    # messages.success(request, ("Stock has been deleted!"))
    return redirect('watchlist')


def transactions(request):
    transactions = Transaction.objects.filter(portfolio=request.user.portfolio).order_by('date')

    return render(request, 'transactions.html', {'transactions': transactions})



