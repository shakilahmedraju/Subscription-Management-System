from django.contrib import admin
from django.urls import path, include

from subscriptions import views as subscriptions_views

urlpatterns = [    
    path('api/subscribe/', subscriptions_views.SubscribeView.as_view(), name='subscribe'),
    path('api/subscriptions/', subscriptions_views.SubscriptionListView.as_view(), name='subscriptions'),
    path('api/cancel/', subscriptions_views.CancelSubscriptionView.as_view(), name='cancel'),
    path('api/exchange-rate/', subscriptions_views.ExchangeRateView.as_view(), name='exchange-rate'),
    path('subscriptions/', subscriptions_views.subscription_list_view, name='subscription-list'),
]