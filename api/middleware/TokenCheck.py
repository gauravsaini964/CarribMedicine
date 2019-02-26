# REST Imports.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import jwt
from rest_framework_jwt.authentication import api_settings

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

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
            print('heere')
            if request.META['HTTP_KEY']:
                api_key = request.META['HTTP_KEY']
                try:
                    api_key_obj = AuthKey.objects.get(key=api_key, is_active=True, ends_at__gte=current_timestamp)
                except AuthKey.DoesNotExist:
                    return HttpResponse(json.dumps(res), status.HTTP_400_BAD_REQUEST)
        except:
            return HttpResponse(json.dumps(res), status.HTTP_400_BAD_REQUEST)


        if not request.path.startswith('/v1/auth/'):
            try:
                auth = request.META['HTTP_AUTHORIZATION'].split()[1]
                try:
                    payload = jwt_decode_handler(auth)
                    user_obj = User.objects.get(id=payload.get('sub'), is_logged_in=True, is_active=True)
                    if user_obj:
                        request.requested_by = payload.get('sub')
                except User.DoesNotExist:
                    request.requested_by = None
                    return HttpResponse(json.dumps({'message': 'User is logged out. Login again.'}),
                                        status.HTTP_401_UNAUTHORIZED)      
                except jwt.ExpiredSignature:
                    request.requested_by = None
                    return HttpResponse(json.dumps({'message': 'Signature has expired.'}),
                                        status.HTTP_401_UNAUTHORIZED)
                except jwt.DecodeError:
                    request.requested_by = None
                    return HttpResponse(json.dumps({'message': 'Error decoding signature.'}),
                                        status.HTTP_400_BAD_REQUEST)
                except jwt.InvalidTokenError:
                    request.requested_by = None
                    return HttpResponse(json.dumps({'message': 'Incorrect authentication token.'}),
                                        status.HTTP_401_UNAUTHORIZED)
            except:
                return HttpResponse(json.dumps({'error': 'No Authorization token provided'}),
                                    status.HTTP_401_UNAUTHORIZED)

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response
