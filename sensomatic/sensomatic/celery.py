import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensomatic.settings')

app = Celery('sensomatic')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

"""
This requires celery beat, so dont be a dumb dumb and remember to run it 
with the following command: 

celery -A sensomatic worker -l INFO -B

The "-B" flag is for the beat scheduler, so dont forget it idiot.
And remember API key
"""

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute='*/1'),
        sender.signature('operations.tasks.create_route'),
    )

