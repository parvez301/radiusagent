import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from property_search.utils import PropertySearchBackendService


@csrf_exempt
def property_search(request):
    """This is a django view method
    which get accessed by /search endpoint
    Args:
        request {obj} -- Request Object
    """
    if request.method == "POST":
        # Do Magical Thing
        request_body = json.loads(request.body)
        backend_service = PropertySearchBackendService(request_body)
        response = backend_service.search_properties(request_body)
    else:
        response = {
            'status': False,
            'message': "Only Post requests are supported"
        }
    return HttpResponse(json.dumps(response))
        