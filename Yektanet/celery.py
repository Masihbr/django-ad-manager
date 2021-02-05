import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Yektanet.settings')

app = Celery('Yektanet')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'save-status-every-hour': {
        'task': 'advertiser_management.tasks.save_hourly_ad_status',
        'schedule': crontab(minute=0, hour='*/1'),
        'args': (),
    },
    'save-status-every-day': {
        'task': 'advertiser_management.tasks.save_daily_ad_status',
        'schedule': crontab(minute=0, hour=0),
        'args': (),
    },
}
app.conf.timezone = 'UTC'

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
