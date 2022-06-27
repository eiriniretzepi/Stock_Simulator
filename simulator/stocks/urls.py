from django.urls import path, include
from . import views

urlpatterns = [
    path('portfolio', views.portfolio, name="portfolio"),
    path('stockInfo', views.stock_info, name="stockInfo"),
    path('buy', views.buy, name="buy"),
    path('watchlist', views.watchlist, name="watchlist"),
    # path('buySell', views.buy_sell, name="buySell"),
]
