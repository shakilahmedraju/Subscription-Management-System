# from SubXTracker.celery import app
# from subscriptions.models import ExchangeRateLog
# from django.conf import settings
# import requests

# @app.task
# def fetch_exchange_rate(base_currency, target_currency):
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



from SubXTracker.celery import app


@app.task
def fetch_exchange_rate(base_currency, target_currency):
    from subscriptions.models import ExchangeRateLog
    from django.conf import settings
    import requests

    url = settings.EXCHANGE_RATE_API_URL.format(
            api_key=settings.EXCHANGE_RATE_API_KEY,
            base_currency=base_currency
        )
    # headers = {'Authorization': f'Bearer {settings.EXCHANGE_RATE_API_KEY}' }

    try:
        # response = requests.get(url, headers=headers)
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        rate = data['conversion_rates'].get(target_currency)
        if rate:
            ExchangeRateLog.objects.create(
                base_currency=base_currency,
                target_currency=target_currency,
                rate=rate
            )
            return f"Successfully fetched {base_currency}/{target_currency} rate: {rate}"
        return f"Target currency {target_currency} not found in response"
    
    except requests.RequestException as e:
        return f"Error fetching exchange rate: {str(e)}"
