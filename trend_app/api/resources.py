from trend_app.models import Trend
from import_export import resources
from trend_app.api.utils import delete_files_with_extensions, export_to_json
import logging

logger = logging.getLogger(__name__)

class TrendExportResource(resources.ModelResource):
    """
    Export Resource class for exporting data from Database
    """
    class Meta:
        model = Trend
    
    def after_export(self, queryset, dataset, **kwargs):
        logger.info("\n\tThe data have successfully been exported!")
        return super(TrendExportResource, self).after_export(queryset, dataset, **kwargs)

class TrendImportResource(resources.ModelResource):
    """
    Import Resource class for importing data into Database
    """
    class Meta:
        model = Trend
        use_bulk = True
        batch_size = None
        skip_diff = True
        skip_unchanged = True
        force_init_instance = True
        report_skipped = False
        use_transactions = True
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

    def after_import(self, dataset, result, **kwargs):
        export_to_json()
        delete_files_with_extensions()
        count_imported_data = result.totals.get('new',0)
        logger.info(f"\n\t{count_imported_data} records have successfully been imported!")
        return super(TrendImportResource, self).after_import(dataset, result, **kwargs)

    