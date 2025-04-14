from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from trend_app.models import Trend
from trend_app.api.resources import TrendImportResource

@admin.register(Trend)
class TrendAdmin(ImportExportModelAdmin):
    list_display = ["megatrend",'macrotrend','technology_readiness_level']
    resource_classes = [TrendImportResource]