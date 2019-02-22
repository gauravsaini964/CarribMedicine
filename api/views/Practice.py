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

class QuizInitializeView(APIView):

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
            user_id=user, quiz_type='practice', result_set={}, entity_id=subject['id'], entity_type='subject',
            total_questions=len(final_question_list))
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


class QuizAnswersView(APIView):

    @staticmethod
    def post(request):

        quiz_question_id = request.POST.get('quiz_question_id', None)
        user_choice_id = request.POST.get('user_choice_id', None)
        response_time = request.POST.get('response_time', 0.00)

        quiz_quest_obj = QuizQuestions.objects.filter(id=quiz_question_id).first()
        quiz_obj = Quiz.objects.filter(id=quiz_quest_obj.quiz_id).first()
        correct_choice = Choices.objects.filter(
            questionschoices__question_id=quiz_quest_obj.question_id, questionschoices__is_correct=True).first()
        user_choice = Choices.objects.filter(id=user_choice_id).first()
        question = Questions.objects.filter(id=quiz_quest_obj.question_id).first()

        if correct_choice.id == int(user_choice_id):
            quiz_quest_obj.marks = 1.00
            quiz_obj.marks += 1.00
            quiz_obj.questions_attempted += 1
            quiz_obj.correct_questions += 1
            answered_correctly = True
        else:
            quiz_quest_obj.marks = 0.00
            quiz_obj.questions_attempted += 1
            quiz_obj.incorrect_questions += 1
            answered_correctly = False

        new_response = {
            'question_text': question.text,
            'user_choice_text': user_choice.text,
            'correct_choice_text': correct_choice.text,
            'question_hint': question.hints,
            'response_time': response_time,
            'answered_correctly': answered_correctly}

        quiz_result_set_modify = quiz_obj.result_set
        if quiz_result_set_modify:
            quiz_result_set_modify['question_answer_response'].append(new_response)
        else:
            quiz_result_set_modify['question_answer_response'] = [new_response]

        quiz_quest_obj.user_answer = user_choice
        quiz_quest_obj.correct_answer = correct_choice
        quiz_quest_obj.response_time = response_time
        quiz_quest_obj.save()
        quiz_obj.save()
        res = {
            'message': 'Answer Posted Successfully',
            'result': {'answered_correctly': answered_correctly}}
        return Response(res, status.HTTP_200_OK)


class QuizCompletionView(APIView):

    @staticmethod
    def post(request):

        quiz_id = request.POST.get('quiz_id', None)
        quiz_obj = Quiz.objects.filter(id=quiz_id).first()

        if quiz_obj.is_complete is False:
            
            percentage = (float(quiz_obj.marks)/ float(quiz_obj.total_questions)) * 100.00

            quiz_obj.is_complete = True
            quiz_obj.percentage = percentage

            quiz_result_set_modify = quiz_obj.result_set
            quiz_result_set_modify['total_questions'] = quiz_obj.total_questions
            quiz_result_set_modify['marks'] = quiz_obj.marks
            quiz_result_set_modify['percentage'] = percentage
            quiz_result_set_modify['correct_questions'] = quiz_obj.correct_questions
            quiz_result_set_modify['incorrect_questions'] = quiz_obj.incorrect_questions
            quiz_result_set_modify['total_attempted'] = quiz_obj.questions_attempted

        res = {'message': 'Result compiled successfully', 'result': quiz_obj.result_set}
        quiz_obj.save()
        return Response(res, status.HTTP_200_OK)
