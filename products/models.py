from django.db import models
from django.utils import timezone

class Product(models.Model):
    """
    Product model for the e-commerce application
    """
    product_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    product_description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ['-created_at']