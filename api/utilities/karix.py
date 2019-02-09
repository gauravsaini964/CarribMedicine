from __future__ import print_function
import time
import karix
from karix.rest import ApiException
from karix.configuration import Configuration
from karix.api_client import ApiClient
from pprint import pprint

# Configure HTTP basic authorization: basicAuth
config = Configuration()
config.username = '2827109c-2984-4142-97d8-e03c4f73e915'
config.password = '864f8a8f-590f-44f4-ba2c-7bf6039ffa1b'
# create an instance of the API class
api_instance = karix.MessageApi(api_client=ApiClient(configuration=config))

def send_otp(destination_phone_no, otp):
    message = karix.CreateMessage(
        source="9999924738", destination=[str(destination_phone_no)],
        text="Your Carrib Login OTP is <{}>".format(str(otp)))
    api_response = api_instance.send_message(message=message)
    return api_response

