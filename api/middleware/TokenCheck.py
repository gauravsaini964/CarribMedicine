# REST Imports.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.http import HttpResponse

# MISC Imports.
import time
import datetime
import json

# Models Imports.
from api.models import User, AuthKey


class KeyAndTokenCheck:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        res = {'message': 'Api Key Invalid.'}
        request.start_time = time.time()
        current_timestamp = datetime.datetime.now()
        try:
            if request.META['HTTP_KEY']:
                api_key = request.META['HTTP_KEY']
                try:
                    api_key_obj = AuthKey.objects.get(key=api_key, is_active=True, ends_at__gte=current_timestamp)
                except AuthKey.DoesNotExist:
                    return HttpResponse(json.dumps(res), status=HTTP_400_BAD_REQUEST)
        except:
            return HttpResponse(json.dumps(res), status=HTTP_400_BAD_REQUEST)

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response
