from django.contrib import admin

from . import models


class PredictionsAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Predictions, PredictionsAdmin)