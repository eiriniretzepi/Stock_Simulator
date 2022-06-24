from django.shortcuts import render
from .models import Portfolio, Stock, Transaction, Watchlist, Alert


def list(request):
    portfolio = Portfolio.objects.all()
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


def buy(request, buy):
    import yfinance as yf

    # if request.method == 'POST':

    return render(request, 'buy.html', {'buy': buy})


# def sell(request):
#     import yfinance as yf
#
#     # if request.method == 'POST':
#
#     return render(request, 'buy.html', {'buy': buy})

