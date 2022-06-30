from django.db import models
from django.contrib.auth.models import User


class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cash = models.FloatField(default=20000.0, editable=True)
    cashInvested = models.FloatField(default=0.0, editable=True)


class Stock(models.Model):
    name = models.CharField(max_length=20)
    ticker = models.CharField(max_length=20)
    date = models.DateField()
    priceBought = models.FloatField()
    stocksBought = models.IntegerField()
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)


class AllStocks(models.Model):
    name = models.CharField(max_length=20)
    ticker = models.CharField(max_length=20)
    totalCost = models.FloatField()
    stocksOwned = models.IntegerField()
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)


class Transaction(models.Model):
    stockName = models.CharField(max_length=20)
    bought = models.BooleanField(default=True)
    numberOfStocks = models.IntegerField()
    stockPrice = models.FloatField()
    date = models.DateField()
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)


class Watchlist(models.Model):
    ticker = models.CharField(max_length=20)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)



