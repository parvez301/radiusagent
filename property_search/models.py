from django.db import models

# Create your models here.
class PropertyDetail(models.Model):
    """Property Model
    """
    lat = models.CharField(max_length=250)
    lng = models.CharField(max_length=250)
    bedroom = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
