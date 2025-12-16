from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class Product(models.Model):
    """
    Product model for the e-commerce application with rating enhancement
    """
    product_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    product_description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    def __str__(self):
        return self.product_name

    @property
    def calculated_average_rating(self):
        """
        On-the-fly calculation of average rating
        """
        ratings = self.reviews.values_list('rating', flat=True)
        if ratings:
            return round(sum(ratings) / len(ratings), 2)
        return None

    def update_average_rating(self):
        """
        Method to explicitly update average rating
        """
        self.average_rating = self.calculated_average_rating
        self.save(update_fields=['average_rating'])

    class Meta:
        ordering = ['-created_at']

class Review(models.Model):
    """
    Review model for products
    """
    product = models.ForeignKey(
        Product,
        related_name='reviews',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review for {self.product.product_name} by {self.user.username}"

    class Meta:
        unique_together = ['product', 'user']
        ordering = ['-created_at']