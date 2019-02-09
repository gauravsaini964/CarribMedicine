# REST Imports.
from rest_framework.views import APIView

# MISC Imports.
import time
import datetime

# def jwt_payload_handler(user):
#     """ Custom payload handler
#     Token encrypts the dictionary returned by this function, and can be decoded by rest_framework_jwt.utils.
#       jwt_decode_handler
#     """
#     epoch_time = int(time.time())
#     india_time = datetime.datetime.fromtimestamp(epoch_time)
#     expiry_time = india_time + api_settings.JWT_EXPIRATION_DELTA
#     return {
#         'sub': user.id,
#         'iss': api_settings.JWT_ISSUER,
#         'exp': expiry_time,
#         'iat': int(time.time()),
#         'nbf': int(time.time()),
#     }
