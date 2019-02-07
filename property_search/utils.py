import json
import requests

from elasticsearch import Elasticsearch
from decimal import Decimal

from property_search.lib.elastic import get_elastic_connection
from property_search.const import ES_INDEX


class PropertySearchBackendService:
    def __init__(self, data):
        self.lat = data.get('lat')
        self.lon = data.get('lon')
        self.min_price = data.get('min_budget')
        self.max_price = data.get('max_budget')
        self.min_bedrooms = data.get('min_bedrooms')
        self.max_bedrooms = data.get('max_bedrooms')
        self.min_bathrooms = data.get('min_bathrooms')
        self.max_bathrooms = data.get('max_bathrooms')

    def search_properties(self, data):
        """Util method to search properties
        Args:
            data {dict} -- request data

        Returns:
            response {dict} -- API Response
        """
        response = {
            'status': False,
        }
        es = get_elastic_connection()
        query = self.get_elastic_query()
        try:
            search_results = es.search(
                index=ES_INDEX,
                body=query
            )
            properties = search_results.get('hits').get('hits')
            results = self.get_properties_result(properties)
            if results:
                response = {
                    'status': True,
                    'results': results
                }
            else:
                response = {
                    'status': True,
                    'results': [],
                    'message': "No Results Found"
                }
        except Exception as e:
            # TODO: need to enable logger for this projecy
            # Which will keep logging all such exceptions and
            # keep printing the useful results
            print('Exception Occured while fetching the elastic search results')
        
        return response

    def get_properties_result(self, properties):
        """Get properties Resultres
        Arg:
            properties {list} -- List Of Results
        """
        results = []
        for prop in properties:
            results.append({
                'property_name': prop.get('_source').get('property_name'),
                'price': prop.get('_source').get('price'),
                'no_of_bedrooms': prop.get('_source').get('bedrooms'),
                'no_of_bathrooms': prop.get('_source').get('bathrooms'),
                'city': prop.get('_source').get('city'),
                'match_score': self.get_match_score(prop),
                'distance_from_user': "{0:.2f}".format(prop.get('sort')[0])
            })

        return results

    def get_match_score(self, prop):
        """This method calculate the match score of property
        according to user's search params
        Args:
            prop {dict} -- property dict
        Returns
            match_score {float} - match score for property
        """
        match_score = 0.0

        # Calculate Match Score on the basis on property distance from user
        user_distance_from_property = prop.get('sort')[0]
        if user_distance_from_property <= 2:
            match_score += 30.0
        elif 3 <= user_distance_from_property <= 10:
            # About this formula
            # So here we assumed that for 2 miles match percentage for distance will be 30%
            # But for property which is in 3 to 10 we will calulate the
            # percentage on scale of 1 to 8
            # So first we calculate the percentage of how far the property
            # Is from user's distance than we calculate the actual
            # Match score on the basis of match_score_weightage_mapping
            # which In this case will be 30%
            match_score += (((user_distance_from_property/8)*100)*(30/100))

        # For rest of the parameters weightage will be full
        # Because we have already filtered out the properties which
        # Lies outside the search criteria
        match_score += 30.0 + 20.0 + 20.0

        return match_score

    def get_elastic_query(self):
        """Prepares the elastic search query
        """
        query = {
            "sort": [
                {
                    "_geo_distance": {
                        "location": {
                            "lat": self.lat,
                            "lon": self.lon
                        },
                        "order": "asc",
                        "unit": "mi"
                    }
                }
            ], 
            "query": {
                "bool": {
                "must": [
                    {
                        "range": {
                            "price": {
                                "gte": (self.min_price - (0.10 * self.min_price)),
                                "lte": (self.max_price + (0.10 * self.max_price))
                            }
                        }
                    },
                    {
                        "range": {
                            "bedrooms": {
                                "gte": self.min_bedrooms,
                                "lte": self.max_bedrooms
                            }
                        }
                    },
                    {
                    "range": {
                            "bathrooms": {
                                "gte": self.min_bathrooms,
                                "lte": self.max_bathrooms
                            }
                        }
                    }
                ],
                "filter": {
                    "geo_distance": {
                        "distance": "100mi",
                        "location": {
                            "lat": self.lat,
                            "lon": self.lon
                        }
                    }
                }
                }
            }
            }
        return query


    