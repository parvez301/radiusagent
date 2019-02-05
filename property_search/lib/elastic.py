from django.conf import settings

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Integer, Text, GeoPoint
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers
from property_search.models import *

from property_search.const import ES_MAX_RETRIES, RETRY_ON_TIMEOUT, ES_INDEX

# Create a connection to ElasticSearch
connections.create_connection()

# ElasticSearch "model" mapping out what fields to index
class PropertyIndex(DocType):
    property_name = Text()
    city = Text()
    location = GeoPoint()
    price = Integer()
    no_of_bedrooms = Integer()
    no_of_bathrooms = Integer()

    class Meta:
        index = ES_INDEX
        type = 'doc'

# Bulk indexing function, run in shell
def bulk_indexing():
    PropertyIndex.init(index=ES_INDEX)
    es = get_elastic_connection()

    bulk(client=es, actions=(b.indexing() for b in PropertyDetail.objects.all().iterator()))

def get_elastic_connection():
    """Set up connection with elastic search
    Returns:
        es - ElasticClient Object
    """
    if settings.ES_SCHEME == 'http':
        es = Elasticsearch(hosts=[{'host': settings.ES_HOST, 'port': int(settings.ES_PORT)}],
                            use_ssl=False, verify_certs=False, scheme=settings.ES_SCHEME,
                            connection_class=RequestsHttpConnection,
                            max_retries=ES_MAX_RETRIES, retry_on_timeout=RETRY_ON_TIMEOUT)
    else:
        es = Elasticsearch(hosts=[{'host': settings.ES_HOST, 'port': int(settings.ES_PORT)}],
                            use_ssl=False, verify_certs=True, scheme=settings.ES_SCHEME,
                            connection_class=RequestsHttpConnection,
                            max_retries=ES_MAX_RETRIES, retry_on_timeout=RETRY_ON_TIMEOUT)

    return es