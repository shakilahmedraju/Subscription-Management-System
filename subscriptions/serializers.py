from rest_framework import serializers
from .models import Plan, Subscription, ExchangeRateLog


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'duration_days']

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.all(),
        source='plan',
        write_only=True
    )
    
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'plan', 'plan_id', 'start_date', 'end_date', 'status']
        read_only_fields = ['user', 'start_date', 'end_date', 'status']

class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRateLog
        fields = ['base_currency', 'target_currency', 'rate', 'fetched_at']
        read_only_fields = ['rate', 'fetched_at']