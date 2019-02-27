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
    User, UserPracticePaperScore, UserSubjectScore, PracticePapers)


class LeaderboardView(APIView):

    @staticmethod
    def post(request):
        practice_paper_id = request.POST.get('practice_paper_id')
        user = request.requested_by
        if not practice_paper_id:
            res = {'message': 'Practice Paper ID required'}
            return Response(res, status.HTTP_400_BAD_REQUEST)
        
        prac_paper_leaderboard = UserPracticePaperScore.objects.filter(practice_paper_id=practice_paper_id).\
            values('score', 'practice_paper__name', 'user_id', 'user__first_name').order_by('-score')

        rank = 1
        requester_info = None
        
        for obj in prac_paper_leaderboard:
            obj['rank'] = rank
            rank + 1
            if obj['user_id'] == user:
                requester_info = obj
        
        if not requester_info:
            user_obj = User.objects.filter(id=user).first()
            prac_paper_obj = PracticePapers.objects.filter(id=practice_paper_id).first()
            requester_info = {
                "rank": -1,
                "user_id": user_obj.id,
                "score": -1,
                "practice_paper__name": prac_paper_obj.name,
                "user__first_name": user_obj.first_name}

        res = {
            "message": "Leaderboard compiled successfully",
            "result": {
                "leaderboard": prac_paper_leaderboard,
                "requester_info": requester_info}}
        return Response(res, status.HTTP_200_OK)