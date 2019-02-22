# REST Imports.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth.hashers import check_password

# MISC Imports.
import datetime

# Models Imports.
from api.models import User, Subjects

# Serializer Imports.


class TabList(APIView):

    @staticmethod
    def get(request):

        user = request.requested_by
        # harcode for now
        tabs = [
            {
                'tab_id': 1,
                'tab_name': 'Learn',
                'visibility': 'public',
                'is_visible': True
            },
            {
                'tab_id': 2,
                'tab_name': 'Practice',
                'visibility': 'public',
                'is_visible': True
            },
            {
                'tab_id': 3,
                'tab_name': 'Assessments',
                'visibility': 'public',
                'is_visible': True
            }, ]

        res = {'message': 'TabList fetched successfully', 'result': {'tabs_list': tabs}}
        return Response(res, status.HTTP_200_OK)


class SubjectList(APIView):

    @staticmethod
    def get(request):
        user = request.requested_by
        subject_list = Subjects.objects.all().values()
        res = {'message': 'Subject List fetched successfully', 'result': {'tabs_list': subject_list}}
        return Response(res, status.HTTP_200_OK)
