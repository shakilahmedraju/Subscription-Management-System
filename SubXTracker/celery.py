# import os
# from celery import Celery
# from django.conf import settings

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SubXTracker.settings')

# app = Celery('SubXTracker')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()

# @app.on_after_finalize.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(
#         3600.0,  # Every hour
#         fetch_exchange_rate.s('USD', 'BDT'),
#         name='fetch usd to bdt rate hourly'
#     )

# @app.task
# def fetch_exchange_rate(base_currency, target_currency):
#     from subscriptions.models import ExchangeRateLog
#     from django.conf import settings
#     import requests
    
#     url = settings.EXCHANGE_RATE_API_URL.format(base_currency=base_currency)
#     # headers = {'Authorization': f'Bearer {settings.EXCHANGE_RATE_API_KEY}'}
    
#     try:
#         # response = requests.get(url, headers=headers)
#         response = requests.get(url)

#         response.raise_for_status()
#         data = response.json()
        
#         rate = data['rates'].get(target_currency)
#         if rate:
#             ExchangeRateLog.objects.create(
#                 base_currency=base_currency,
#                 target_currency=target_currency,
#                 rate=rate
#             )
#             return f"Successfully fetched {base_currency}/{target_currency} rate: {rate}"
#         return f"Target currency {target_currency} not found in response"
    
#     except requests.RequestException as e:
#         return f"Error fetching exchange rate: {str(e)}"


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
