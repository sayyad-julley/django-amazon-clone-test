from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review, Product

@receiver([post_save, post_delete], sender=Review)
def update_product_rating(sender, instance=None, created=False, **kwargs):
    """
    Signal handler to update product's average rating after review changes
    """
    try:
        product = instance.product if instance else None
        if product:
            # Update average rating
            product.average_rating = product.calculated_average_rating
            product.save(update_fields=['average_rating'])
    except Exception as e:
        # Log the exception or handle it appropriately
        print(f"Error updating product rating: {e}")