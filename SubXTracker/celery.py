import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SubXTracker.settings')

app = Celery('SubXTracker')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Import the task
from subscriptions.tasks import fetch_exchange_rate

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        3600.0,  # Every hour
        fetch_exchange_rate.s('USD', 'BDT'),
        name='fetch usd to bdt rate hourly'
    )
