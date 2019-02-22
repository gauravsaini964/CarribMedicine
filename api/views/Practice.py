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
    User, Subjects, Questions, Choices, QuestionsSubject, QuestionsChoices, Quiz, QuizQuestions)

# Serializer Imports.

class QuizInitialize(APIView):

    @staticmethod
    def post(request):
        user = 4
        subject_id = request.POST.get('subject_id', None)
        if not subject_id:
            res = {'message': 'Subject ID not found'}
            return Response(res, status.HTTP_200_OK)
        subject = Subjects.objects.filter(id=subject_id).values().first()
        questions_list = QuestionsSubject.objects.filter(subject_id=subject_id, question__flag=1).values_list(
            'question_id', flat=True)
        questions = Questions.objects.filter(
            id__in=questions_list, flag=True, question_type=1, text__isnull=False).order_by('?')[:10]
        final_question_list = questions.values_list('id', flat=True)
        
        quiz_obj = Quiz.objects.create(
            user_id=user, quiz_type='practice', result_set={}, entity_id=subject['id'], entity_type='subject')
        final_questions = []
        for question_id in final_question_list:
            quiz_questions = QuizQuestions.objects.create(quiz_id=quiz_obj.id, question_id=question_id)
            question_obj = Questions.objects.filter(id=question_id).values().first()
            question_choices = QuestionsChoices.objects.filter(
                question_id=question_id).values(
                    'choice__text', 'choice__media_url', 'choice__media_type', 'choice__choice_type', 'choice__hints',
                    'choice_id', 'is_correct')
            temp_dict = {'question': question_obj, 'choices': question_choices, 'quiz_question_id': quiz_questions.id}
            final_questions.append(temp_dict)
        final_quiz_data = {'quiz_id': quiz_obj.id, 'questions': final_questions}
        res = {
            'message': 'Quiz generated successfully',
            'result': final_quiz_data}
        return Response(res, status.HTTP_200_OK)

