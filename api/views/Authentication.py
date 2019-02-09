# REST Imports.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth.hashers import check_password

# MISC Imports.
import time
import datetime
from random import randint
from api.utilities.karix import send_otp

# Models Imports.
from api.models import User

# Serializer Imports.


class ListUser(APIView):

    @staticmethod
    def get(request):
        return Response({'result': User.objects.all().values()}, status.HTTP_200_OK)


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.POST.get('email', None)
        if email:
            password = request.POST.get('password', None)
            if User.objects.create_user(email=email, password=password):
                res = {'message': 'User created successfully'}
                return Response(res, status.HTTP_201_CREATED)
        
        if not email:
            phone_no = request.POST.get('phone_no', None)
            if not phone_no:
                res = {'message': 'Phone/Email field is required'}
                return Response(res, status.HTTP_400_BAD_REQUEST)
            else:
                if User.objects.create_user_otp_based(phone=phone_no):
                    res = {'message': 'User created successfully'}
                    return Response(res, status.HTTP_201_CREATED)


class GenerateOTPView(APIView):

    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        phone_no = request.POST.get('phone_no', None)
        try:
            UserObj = User.objects.get(phone_no=phone_no)
            otp = randint(000000, 999999)
            otp_response = send_otp(UserObj.phone_no, otp)
            if otp_response:
                UserObj.otp = otp
                UserObj.save()
            res = {'message': 'OTP sent successfully '}
        except User.DoesNotExist:
            res = {'message': "User Doesnt exist"}
            return Response(res, status.HTTP_404_NOT_FOUND)
        return Response(res, status.HTTP_200_OK)


class UserLoginView(APIView):

    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        email = request.POST.get('email', None)
        if email:
            password = request.POST.get('password', None)
            try:
                user_obj = User.objects.get(email=email)
                if check_password(password, user_obj.password):
                    user_obj.is_active = True
                    res = {
                        'message': 'User login successfull',
                        'result': {
                            'user_details': User.objects.filter(email=email).values('id', 'email').first(),
                            'token': user_obj.token,
                            'extra_details': {}}}
                    user_obj.save()
                else:
                    res = {'message': 'User login failed', 'result': {}}
            except User.DoesNotExist:
                res = {'message': 'User doesnt exist', 'result': {}}
            return Response(res, status.HTTP_200_OK)
        else:
            phone_no = request.POST.get('phone_no', None)
            if not phone_no:
                res = {'message': 'Phone/Email field is required'}
                return Response(res, status.HTTP_400_BAD_REQUEST)
            else:
                otp = request.POST.get('otp', None)
                try:
                    user_obj = User.objects.get(phone_no=phone_no)
                    if int(otp) == user_obj.otp:
                        user_obj.is_active = True
                        res = {
                            'message': 'User login successfull',
                            'result': {
                                'user_details': User.objects.filter(phone_no=phone_no).values('id', 'email').first(),
                                'token': user_obj.token,
                                'extra_details': {}}}
                        user_obj.save()
                    else:
                        res = {'message': 'User login failed', 'result': {}}
                except User.DoesNotExist:
                    res = {'message': 'User doesnt exist', 'result': {}}
                return Response(res, status.HTTP_200_OK)

