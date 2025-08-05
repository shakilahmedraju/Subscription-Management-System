from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db import transaction
from django.shortcuts import render
from .models import Plan, Subscription, ExchangeRateLog
from .serializers import PlanSerializer, SubscriptionSerializer, ExchangeRateSerializer
import requests
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Check if user already has an active subscription
            active_sub = Subscription.objects.filter(
                user=request.user,
                status='active'
            ).exists()
            
            if active_sub:
                return Response(
                    {'error': 'You already have an active subscription'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            subscription = serializer.save(user=request.user)
            return Response(SubscriptionSerializer(subscription).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubscriptionListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer
    
    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

class CancelSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        subscription_id = request.data.get('subscription_id')
        if not subscription_id:
            return Response(
                {'error': 'subscription_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            subscription = Subscription.objects.get(id=subscription_id)
        except Subscription.DoesNotExist:
            return Response({'error': 'Active subscription not found'},status=status.HTTP_404_NOT_FOUND)
            
        subscription.status = 'cancelled'
        subscription.save()
        return Response({'status': 'subscription cancelled'})
    


class ExchangeRateView(APIView):
    def get(self, request):
        base_currency = request.query_params.get('base', 'USD').upper()
        target_currency = request.query_params.get('target', 'BDT').upper()
        
        # Try to get from database first
        latest_rate = ExchangeRateLog.objects.filter(
            base_currency=base_currency,
            target_currency=target_currency
        ).order_by('-fetched_at').first()
        
        if latest_rate:
            return Response(ExchangeRateSerializer(latest_rate).data)
        
        # If not in DB, fetch from API
        url = settings.EXCHANGE_RATE_API_URL.format(
            api_key=settings.EXCHANGE_RATE_API_KEY,
            base_currency=base_currency
        )

        # headers = {'Authorization': f'Bearer {settings.EXCHANGE_RATE_API_KEY}'}
        
        try:
            # response = requests.get(url, headers=headers)
            response = requests.get(url)

            response.raise_for_status()
            data = response.json()

            # print("data=======", data)
            
            rate = data['conversion_rates'].get(target_currency)
            if not rate:
                return Response(
                    {'error': f'Target currency {target_currency} not found'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Save to database
            exchange_rate = ExchangeRateLog.objects.create(
                base_currency=base_currency,
                target_currency=target_currency,
                rate=rate
            )
            
            return Response(ExchangeRateSerializer(exchange_rate).data)
            
        except requests.RequestException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

def subscription_list_view(request):
    subscriptions = Subscription.objects.select_related('user', 'plan').all()
    return render(request, 'subscriptions/list.html', {'subscriptions': subscriptions})