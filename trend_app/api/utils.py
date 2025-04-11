from django_celery_beat.models import PeriodicTask, IntervalSchedule
import tablib
from django.conf import settings
import datetime
import glob
import json
import os


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

def update_headers():
    """
    Modify the header of the csv file to conform with python naming convention 
    """
    with open('random_data.csv', 'r') as csv_file:
        dataset = tablib.Dataset().load(csv_file, format='csv', delimiter=';')
        dataset.headers = new_headers
        with open('updated_data.csv', 'w', encoding='utf-8', newline='') as f:
                f.write(dataset.export('csv'))


def import_csv():
    """
    Import the csv data into DB 
    """
    from trend_app.api.resources import TrendImportResource
    update_headers()
    resource = TrendImportResource()

    with open('updated_data.csv','r', encoding='utf-8') as file:
        data = tablib.Dataset().load(file.read(), format='csv')
    resource.import_data(data, dry_run=False, raise_errors=True)


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
    schedule= IntervalSchedule.objects.filter(every=1, period=IntervalSchedule.HOURS).first()
    args = json.dumps([])

    if not schedule:
        schedule = IntervalSchedule.objects.create(every=1, period=IntervalSchedule.HOURS)

    periodic_task, created = PeriodicTask.objects.get_or_create(
            name = 'Database Periodic Update',
            crontab = schedule,
            args = args,
            task = "trend_app.api.tasks.import_csv_to_db"
    )


def delete_files_with_extensions(csv_file_path=settings.BASE_DIR, file_extensions=[".csv"]):
    """
        Delete the cvs file after the data have been imported  
    """
#     file_name, _ = os.path.splitext(source)
#     file_name = os.path.basename(file_name)

    if os.name == "nt":
        csv_file_path = settings.BASE_DIR.replace("\\", "/")

    for extension in file_extensions:
        # file_suffix = f"{file_name}" + f"{extension}"

        path = os.path.join(csv_file_path, f"*{extension}")
        # path = "*{extension}"
        
        csv_files_to_delete = glob.glob(path)
        print('patern',path)
        print("found",csv_files_to_delete)
        # if csv_files_to_delete:
        #     for file in csv_files_to_delete:
        #         try:
        #             os.remove(file)
        #         except Exception as e:
        #             print(f"Error deleting {file}: {e}")