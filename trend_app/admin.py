from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from trend_app.models import Trend

class TrendResource(resources.ModelResource):
    """
    Resource class for importing data into Database form admin 
    """
    class Meta:
        model = Trend
        exclude = ('id','uploaded_at','updated_at',)
        import_id_fields = (
            'megatrend',
            'macrotrend',
            'challenges_and_research_gaps',
            'total_count_of_publications',
            'total_count_of_patents',
            'technology_readiness_level',
            'impact_strength',
            'steepl',
            'relevant_industries',
            'real_world_application_and_use_cases',
        )

@admin.register(Trend)
class TrendAdmin(ImportExportModelAdmin):
    resource_classes = [TrendResource]