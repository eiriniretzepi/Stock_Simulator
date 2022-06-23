from django import forms
from .models import Portfolio, Stock, Transaction, Watchlist, Alert


class PortolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ["cash", "cashInvested"]


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["name", "stocksOwned", "priceBought", "portfolio"]


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["stockName", "bought", "numberOfStocks", "stockPrice", "date", "portfolio"]


class WatchlistForm(forms.ModelForm):
    class Meta:
        model = Watchlist
        fields = ["stockName", "portfolio"]


class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ["stockName", "alertPrice", "portfolio"]
