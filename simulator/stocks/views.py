from django.shortcuts import render
from .models import Portfolio, Stock, Transaction, Watchlist, Alert


def list(request):
    portfolio = Portfolio.objects.all()
    if request.method == 'POST':
        buy = request.POST['buy']
        shares = request.POST['numberOfShares']

    return render(request, 'portfolio.html', {'portfolio': portfolio, 'shares': shares})


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


# def buy_sell(request):
#     return render(request, 'portfolio.html', {})


# def sell(request):
#     import yfinance as yf
#
#     # if request.method == 'POST':
#
#     return render(request, 'buy.html', {'buy': buy})

