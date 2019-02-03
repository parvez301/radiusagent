from django.db import models
from django.utils import timezone
from property_search.const import ES_INDEX

from django.db.models.signals import post_save
from django.dispatch import receiver

from property_search.lib.elastic import PropertyIndex


# Create your models here.
class PropertyDetail(models.Model):
    """Property Model
    """
    lat = models.CharField(max_length=250)
    lon = models.CharField(max_length=250)
    no_of_bedrooms = models.IntegerField(default=0)
    no_of_bathrooms = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateField(default=timezone.now)
    modified_at = models.DateField(default=timezone.now)

    class Meta:
        db_table = 'property_detail'

    # Method for indexing the model
    def indexing(self):
        obj = PropertyIndex(
            meta={'id': self.lat},
            geo=[self.lat, self.lon],
            price=self.price,
            no_of_bedrooms=self.no_of_bedrooms,
            no_of_bathroomst=self.no_of_bathrooms
        )
        obj.save(index=ES_INDEX)
        return obj.to_dict(include_meta=True)


# Signal to save each new blog post instance into ElasticSearch
@receiver(post_save, sender=PropertyDetail)
def index_post(sender, instance, **kwargs):
    print(instance)
    instance.indexing()