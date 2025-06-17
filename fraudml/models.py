from django.db import models
from django.conf import settings  # ✅ This will point to AUTH_USER_MODEL

class Transaction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ✅ Correct dynamic user model reference
        on_delete=models.CASCADE,
        related_name="transactions",
        null=True,
        blank=True
    )
    is_fraud = models.BooleanField(null=True, blank=True)  # ✅ Human tag
    customer_id = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100)
    amount = models.FloatField()
    payment_method = models.CharField(max_length=50)
    timestamp = models.DateTimeField()
    device = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    # From AI model
    fraud_probability = models.FloatField(null=True, blank=True)
    
    def fraud_label(self):
        if self.is_fraud is True:
            return "🚨 Fraud"
        elif self.is_fraud is False:
            return "✅ Not Fraud"
        return "⚠️ Not Labeled"
    
    def __str__(self):
        return f"{self.order_id} - {self.customer_id}"
    

class UploadedModel(models.Model):
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    model_file = models.FileField(upload_to='models/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Model uploaded at {self.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}"