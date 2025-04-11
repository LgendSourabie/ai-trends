import glob
import os
from django.conf import settings
from trend_app.api.resources import TrendImportResource
from celery import shared_task
import tablib
from celery import Task
from trend_app.api.utils import update_headers
from django_celery_results.models import TaskResult

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
    path = os.path.join(settings.BASE_DIR, f"*.csv")
        
    folder_csv_files = glob.glob(path)
    if len(folder_csv_files)>0:
        update_headers(file_name=os.path.basename(folder_csv_files[0]))
        resource = TrendImportResource()

        with open('updated_data.csv','r', encoding='utf-8') as file:
            data = tablib.Dataset().load(file.read(), format='csv')
        resource.import_data(data, dry_run=False, raise_errors=True)
