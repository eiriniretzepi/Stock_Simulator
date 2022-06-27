from django.shortcuts import render, redirect
from .models import Portfolio, Stock, Transaction, Watchlist, Alert
from .forms import PortolioForm, StockForm, TransactionForm, WatchlistForm, AlertForm


def portfolio(request):
    portfolio = Portfolio.objects.all()

    if request.method == 'POST':
        buy = request.POST['buy']
        shares = request.POST['numberOfShares']
        ticker = request.POST['ticker']

    return render(request, 'portfolio.html', {'portfolio': portfolio})


def stock_info(request):
    import yfinance as yf

    if request.method == "POST":
        get_ticker = request.POST['ticker']

        ticker = yf.Ticker(get_ticker)
        api = ticker.info

        if api.get("currentPrice") is None:
            api = "Error"

    return render(request, 'stock_info.html', {'api': api})


def buy(request):
    import yfinance as yf

    if request.method == 'POST':
        get_ticker = request.POST['ticker']
        ticker = yf.Ticker(get_ticker)
        api = ticker.info

    # also pass the portfolio available cash in order to check if the purchase is possible
    cash = request.user.portfolio.cash

    return render(request, 'buy.html', {'api': api, 'cash': cash})


def watchlist(request):
    import yfinance as yf

    # if request.method == "POST":
    #     #should check if the stock already exists SHOULD NOT ADD THE SAME STOCK TWICE
    #     pred_ticker = Watchlist.objects.all().values('ticker')
    #     for pred in pred_ticker:
    #         if pred['ticker'] == request.POST:
    #             return redirect('predictions')
    #
    #     form = WatchlistForm(request.POST or None, request.user.portfolio)
    #
    #     if form.is_valid():
    #         object = form.save(commit=False)
    #         object.user = request.user
    #         object.save()
    #         return redirect('watchlist')
    # else:
    #     watchstocks = Watchlist.objects.all()
    #     output = []
    #     for stock in watchstocks:
    #         tick = yf.Ticker(str(stock))
    #         api = tick.info
    #
    #         # if api.get("currentPrice") is None:
    #         #     api = "Error"
    #         # else:
    #         output.append(api)

    return render(request, 'watchlist.html', {})

