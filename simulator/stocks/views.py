from django.shortcuts import render, redirect
from .models import Portfolio, Stock, Transaction, Watchlist, AllStocks
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

    portfolio = request.user.portfolio

    portfolios = Portfolio.objects.filter(user=request.user)
    if not portfolios:
       return redirect('addPortfolio')

    if request.method == 'POST':
        buy = request.POST['buy']
        shares = request.POST['numberOfShares']
        get_ticker = request.POST['ticker']
        ticker = yf.Ticker(get_ticker)
        api = ticker.info

        if buy == "buy":
            s = Stock.objects.create(name=api.get('longName'),
                                     ticker=get_ticker,
                                     date=datetime.today(),
                                     priceBought=api.get('currentPrice'),
                                     stocksBought=shares,
                                     portfolio=request.user.portfolio)
            s.save()

            buybool = True
            portfolio.cash = portfolio.cash - float(shares)*api.get('currentPrice')
            portfolio.cashInvested = portfolio.cashInvested + float(shares) * api.get('currentPrice')
            portfolio.save()

            # check if stock exists, if it does just change its fields else add a new AllStocks model
            p = AllStocks.objects.filter(portfolio=portfolio)
            existingStocks = p.filter(ticker=get_ticker)

            if existingStocks:
                stock = existingStocks[0]
                stock.totalCost = stock.totalCost + float(shares) * api.get('currentPrice')
                stock.stocksOwned = stock.stocksOwned + int(shares)
                stock.save()
            else:
                addStock = AllStocks.objects.create(name=api.get('longName'),
                                                    ticker=get_ticker,
                                                    totalCost=float(shares)*api.get('currentPrice'),
                                                    stocksOwned=shares,
                                                    portfolio=request.user.portfolio)
                addStock.save()

        else:
            buybool = False
            portfolio.cash = portfolio.cash + float(shares) * api.get('currentPrice')
            portfolio.cashInvested = portfolio.cashInvested - float(shares) * api.get('currentPrice')
            portfolio.save()

            # remove stocks in the AllStocks model from a company also remove from the Stocks
            port = AllStocks.objects.filter(portfolio=portfolio)
            existingStock = port.filter(ticker=get_ticker)
            allstock = existingStock[0]
            allstock.totalCost = allstock.totalCost - float(shares) * api.get('currentPrice')
            allstock.stocksOwned = allstock.stocksOwned - int(shares)
            allstock.save()

            if allstock.stocksOwned == 0:
                allstock.delete()

            stocks = Stock.objects.filter(portfolio=portfolio)
            existingStocks = stocks.filter(ticker=get_ticker).order_by('date')

            #instead of deleting the item it sets the stocksbought to the number we have sold
            stocksSold = 0
            for sold in existingStocks:
                # int(shares) is the number of stocks we are selling
                # stocksSold is the number of shares we have currently sold
                if stocksSold < int(shares):
                    # we want to sell 1 and we have 2
                    if (int(shares)-sold.stocksBought)<0:
                        sold.stocksBought = sold.stocksBought - int(shares)
                        sold.save()
                        stocksSold = int(shares)
                    else:
                        stocksSold = stocksSold + sold.stocksBought
                        sold.delete()

        t = Transaction.objects.create(stockName=api.get('longName'),
                                       bought=buybool,
                                       numberOfStocks=shares,
                                       stockPrice= api.get('currentPrice'),
                                       date=datetime.today(),
                                       portfolio=request.user.portfolio)
        t.save()

    stocks = Stock.objects.filter(portfolio=request.user.portfolio)
    allStocks = AllStocks.objects.filter(portfolio=request.user.portfolio)

    #create a dictionary to make the profit
    currentPrices = []
    for s in stocks:
        ticker = yf.Ticker(s.ticker)
        api = ticker.info
        profit =round(((api.get("currentPrice") - s.priceBought)* s.stocksBought),2)
        currentPrices.append(profit)

    cash = round(request.user.portfolio.cash, 2)
    cashInvested = round(request.user.portfolio.cashInvested, 2)

    return render(request, 'portfolio.html', {'portfolio': request.user.portfolio, 'cash': cash, 'cashInvested': cashInvested, 'stocks': stocks, 'allStocks': allStocks, 'currentPrices': currentPrices})


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
        s = p.filter(ticker=ticker.ticker)

    return render(request, 'stock_info.html', {'api': api, 'stockOwned': s})


def buy(request):
    import yfinance as yf

    if request.method == 'POST':
        get_ticker = request.POST['ticker']
        ticker = yf.Ticker(get_ticker)
        api = ticker.info

    # also pass the portfolio available cash in order to check if the purchase is possible
    cash = round(request.user.portfolio.cash, 2)

    return render(request, 'buy.html', {'api': api, 'cash': cash})


def sell(request):
    import yfinance as yf

    if request.method == 'POST':
        get_ticker = request.POST['ticker']
        ticker = yf.Ticker(get_ticker)
        api = ticker.info

    # extract the number of stocks from AllStocks

    # also pass the portfolio available cash in order to check if the purchase is possible
    cash = round(request.user.portfolio.cash, 2)

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



