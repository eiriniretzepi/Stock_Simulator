from django import forms
from .models import Portfolio, Stock, Transaction, Watchlist, AllStocks


class PortolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ["cash", "cashInvested"]


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["name", "ticker", "date", "priceBought", "stocksBought", "portfolio"]


class AllStockForm(forms.ModelForm):
    class Meta:
        model = AllStocks
        fields = ["name", "ticker", "totalCost", "stocksOwned", "portfolio"]


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["stockName", "bought", "numberOfStocks", "stockPrice", "date", "portfolio"]


class WatchlistForm(forms.ModelForm):
    class Meta:
        model = Watchlist
        fields = ["ticker", "portfolio"]



