from django.db.models.signals import post_save
from django.dispatch import receiver
from trend_app.models import Trend
from celery import chain
import logging

logger = logging.getLogger(__name__)

# def delete_csv_files_after_data_import(sender, instance,created, **kwargs):
    # """
    # Trigger the deletion of csv files after the data have been imported to the DB 
    # """
    # if created:
    #     logger.info("The data have successfully been deleted!")
        # try:
        #     delete_files_with_extensions()
        #     export_to_json()
        #     logger.info("The data have successfully been deleted!")
        # except Exception as e:
        #     logger.info("The data could not be deleted, please retry!")



