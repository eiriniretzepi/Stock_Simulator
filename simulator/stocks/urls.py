from django.urls import path, include
from . import views

urlpatterns = [
    path('portfolio', views.portfolio, name="portfolio"),
    path('addPortfolio', views.addPortfolio, name="addPortfolio"),
    path('stockInfo', views.stock_info, name="stockInfo"),
    path('buy', views.buy, name="buy"),
    path('sell', views.sell, name="sell"),
    path('watchlist', views.watchlist, name="watchlist"),
    path('delete/<stock_id>', views.delete, name="delete"),
    path('transactions', views.transactions, name="transactions"),
    # path('buySell', views.buy_sell, name="buySell"),
]
