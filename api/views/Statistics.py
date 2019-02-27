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
    User, UserPracticePaperScore, UserSubjectScore)


class LeaderboardView(APIView):

    @staticmethod
    def post(request):
        practice_paper_id = request.POST.get('practice_paper_id')

        if not practice_paper_id:
            res = {'message': 'Practice Paper ID required'}
            return Response(res, status.HTTP_400_BAD_REQUEST)
        
        prac_paper_leaderboard = UserPracticePaperScore.objects.filter(practice_paper_id=practice_paper_id).\
            values('score', 'practice_paper__name', 'user_id', 'user__first_name').order_by('-score')

        res = {"message": "Leaderboard compiled successfully", "result": {"leaderboard": prac_paper_leaderboard}}
        return Response(res, status.HTTP_200_OK)