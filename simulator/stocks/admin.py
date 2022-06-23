from django.contrib import admin

from . import models


class PortfolioAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Portfolio, PortfolioAdmin)


class StocksAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Stock, StocksAdmin)


class TransactionsAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Transaction, TransactionsAdmin)


class WatchListAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Watchlist, WatchListAdmin)


class AlertAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Alert, AlertAdmin)