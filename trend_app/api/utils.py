from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.conf import settings
from file_upload.models import FileUpload
import tablib
import datetime
import glob
import json
import os
import logging

logger = logging.getLogger(__name__)

new_headers = [
    'megatrend',
    'macrotrend',
    'challenges_and_research_gaps',
    'total_count_of_publications',
    'total_count_of_patents',
    'technology_readiness_level',
    'impact_strength',
    'steepl',
    'relevant_industries',
    'real_world_application_and_use_cases'
]

def update_headers(file_name):
    """
    Modify the header of the csv file to conform with python naming convention 
    """
    os.makedirs('media', exist_ok=True)
    file_name = os.path.join('media/', file_name)
    with open(file_name, 'r') as csv_file:
        dataset = tablib.Dataset().load(csv_file, format='csv', delimiter=';')
        dataset.headers = new_headers
        output_name = file_name.split('.')[0] + "_updated.csv"
        with open(output_name, 'w', encoding='utf-8', newline='') as f:
                f.write(dataset.export('csv'))
    return output_name


def export_to_json():
    """ 
    Export data to lightweight json format to avoid data lost when
    the app or DB crashes
    """
    from trend_app.api.resources import TrendExportResource
    resource = TrendExportResource()

    export_dir = "db_backup"
    os.makedirs(export_dir, exist_ok=True)
    file_path = os.path.join(export_dir, f"trends_backup_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.json')}")
    with open(file_path, "w") as file:
        db_data = resource.export()
        file.write(db_data.json)


def set_up_data_import_to_db():
    """Import csv data to database every 1 hours
       in case new data are collected
    """
    schedule= IntervalSchedule.objects.filter(every=2, period=IntervalSchedule.MINUTES).first()
    args = json.dumps([])

    if not schedule:
        schedule = IntervalSchedule.objects.create(every=2, period=IntervalSchedule.MINUTES)

    PeriodicTask.objects.get_or_create(
            name = 'Periodic Import of Data',
            interval = schedule,
            args = args,
            task = "trend_app.api.tasks.import_csv_to_db"
    )


def delete_files_with_extensions(csv_file_path=settings.BASE_DIR, file_extensions=[".csv"]):
    """
        Delete the cvs file after the data have been imported  
    """
    for extension in file_extensions:
        path = os.path.join(csv_file_path, f"*{extension}")
        
        csv_files_to_delete = glob.glob(path)
        if csv_files_to_delete:
            for file in csv_files_to_delete:
                try:
                    os.remove(file)
                    logger.info(f"\n\t{os.path.basename(file)} have successfully been removed!")
                except Exception as e:
                    logger.error(f"\n\tError when deleting {file}: {e}")
    FileUpload.objects.all().delete()
                 