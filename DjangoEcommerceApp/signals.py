from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ProductReviews, Products

def update_product_rating(product):
    """
    Helper function to update product's average rating
    Calculates the average rating from active reviews and saves to the product
    """
    active_reviews = ProductReviews.objects.filter(product_id=product, is_active=1)

    if active_reviews.exists():
        total_rating = sum(float(review.rating) for review in active_reviews)
        average_rating = round(total_rating / active_reviews.count(), 2)
    else:
        average_rating = 0.0

    # Directly update average_rating field
    Products.objects.filter(pk=product.pk).update(average_rating=average_rating)

@receiver(post_save, sender=ProductReviews)
def update_rating_on_review_save(sender, instance, created, **kwargs):
    """Update average rating when a review is created or updated"""
    update_product_rating(instance.product_id)

@receiver(post_delete, sender=ProductReviews)
def update_rating_on_review_delete(sender, instance, **kwargs):
    """Update average rating when a review is deleted"""
    update_product_rating(instance.product_id)