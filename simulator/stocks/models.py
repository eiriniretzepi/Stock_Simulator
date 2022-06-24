from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cash = models.IntegerField(default=20000, editable=True)
    cashInvested = models.IntegerField(default=0, editable=True)


class Stock(models.Model):
    name = models.CharField(max_length=50)
    stocksOwned = models.IntegerField()
    priceBought = models.FloatField()  # the price of the stock when it was bought
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)


class Transaction(models.Model):
    stockName = models.CharField(max_length=50)
    bought = models.BooleanField(default=True)
    numberOfStocks = models.IntegerField()
    stockPrice = models.FloatField()
    date = models.DateField()
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)


class Watchlist(models.Model):
    stockName = models.CharField(max_length=50)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)


class Alert(models.Model):
    stockName = models.CharField(max_length=50)
    alertPrice = models.FloatField()
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

