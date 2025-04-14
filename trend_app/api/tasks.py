from trend_app.api.utils import delete_files_with_extensions, update_headers
from django_celery_results.models import TaskResult
from trend_app.api.resources import TrendImportResource
from django.conf import settings
from celery import shared_task
from celery import Task
import tablib
import logging
import glob
import os

logger = logging.getLogger(__name__)

class CustomTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        """Automatically set the task name in TaskResult"""
        task_result = TaskResult.objects.filter(task_id=task_id).first()
        if task_result:
            task_result.task_name = self.name
            task_result.save()
        super().on_success(retval, task_id, args, kwargs)


@shared_task
def import_csv_to_db():
    """
    Import the csv data into DB 
    """
    os.makedirs('media', exist_ok=True)
    path = os.path.join('media/', f"*.csv")
        
    folder_csv_files = glob.glob(path)
    if len(folder_csv_files) == 0:
        logger.info("No file found to be imported.")
        return 0
    for file in folder_csv_files: 
        file_name = os.path.basename(file)
        if not file_name.endswith('_updated.csv'):
            output_file = update_headers(file_name=file_name)
            resource = TrendImportResource()
            with open(output_file,'r', encoding='utf-8') as file:
                data = tablib.Dataset().load(file.read(), format='csv')
            resource.import_data(data, dry_run=False, raise_errors=True)
    delete_files_with_extensions(csv_file_path='media/')