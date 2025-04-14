import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE","trends.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

import configurations
configurations.setup()

app = Celery("trends")
app.config_from_object("django.conf:settings",namespace="CELERY")
app.autodiscover_tasks(['trend_app.api.tasks'])


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Runs when Celery starts"""
    try:
        from trend_app.api.utils import set_up_data_import_to_db
        set_up_data_import_to_db()
    except Exception as e:
        print(f"Error in periodic tasks: {e}")
