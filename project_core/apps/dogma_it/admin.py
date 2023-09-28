# Utils
from django.contrib import admin

# Models
from .models import ITReportModel


@admin.register(ITReportModel)
class ItAdminModel(admin.ModelAdmin):
    """"""
    pass
