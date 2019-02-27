# REST Imports.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth.hashers import check_password

# MISC Imports.
import datetime

# Models Imports.
from api.models import (
    User, Subjects, Questions, Choices, QuestionsSubject, QuestionsChoices, Quiz, QuizQuestions, PracticePapers)

# Serializer Imports.


class PaperListView(APIView):

    @staticmethod
    def get(request):
        paper_list = PracticePapers.objects.filter(flag=True).values()
        res = {'message': 'Practice Paper List fetched successfully', 'result': {'practice_paper_list': paper_list}}
        return Response(res, status.HTTP_200_OK)