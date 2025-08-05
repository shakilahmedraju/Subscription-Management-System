from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Plan(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="The name of the subscription plan")
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Price in USD")  
    duration_days = models.IntegerField(help_text="Duration of the plan in days")

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"
        ordering = ['price']

    def __str__(self):
        return f"{self.name} (${self.price} for {self.duration_days} days)"
    

class Subscription(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions', help_text="User who owns this subscription")
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions', help_text="The plan associated with this subscription")
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', help_text="Current status of the subscription")

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        ordering = ['-start_date']
        
    def __str__(self):
        return f"{self.user.username}'s {self.plan.name} subscription ({self.status})"

    def save(self, *args, **kwargs):
        if not self.pk:  # New subscription
            self.start_date = timezone.now().date()
            self.end_date = self.start_date + timezone.timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)



class ExchangeRateLog(models.Model):
    base_currency = models.CharField(max_length=3, help_text="Base currency code (e.g., USD)")
    target_currency = models.CharField(max_length=3, help_text="Base currency code (e.g., BDT)")
    rate = models.DecimalField(max_digits=19, decimal_places=6, help_text="Exchange rate from base to target currency")
    fetched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Exchange Rate Log"
        verbose_name_plural = "Exchange Rate Logs"
        ordering = ['-fetched_at']

    def __str__(self):
        return f"1 {self.base_currency} = {self.rate} {self.target_currency} at {self.fetched_at}"