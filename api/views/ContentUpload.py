# REST Imports.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

# MISC Imports.
import time
import datetime
import os
import boto
from boto.s3.key import Key

# Models Imports.
from api.models import User, UserDevice, Questions, Choices, QuestionsChoices

# Serializer Imports.
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
CLOUD_FRONT_URL = "https://d32rh8eq5a9604.cloudfront.net/"
REGION_HOST = 's3.ap-south-1.amazonaws.com'


def aws_upload_url(file_obj, folder_name):
    file_extension = file_obj.content_type.split('/')[1]
    random_number = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    file_name = random_number + '.' + file_extension
    prefix = folder_name
    url = CLOUD_FRONT_URL + folder_name + file_name
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, host=REGION_HOST)
    bucket = conn.get_bucket('carrib-bucket')
    full_key_name = prefix + str(file_name)
    k = Key(bucket)
    k.key = full_key_name
    k.set_contents_from_string(file_obj.read())
    return url


class QuestionUpload(APIView):
    
    @staticmethod
    def post(request):
        question_text = request.POST.get('question_text')
        hints = request.POST.get('hint')
        question_type = request.POST.get('question_type')   # 1-mcq
        media_type = request.POST.get('media_type')
        media_url = request.POST.get('media_url')
        flag = request.POST.get('flag')
        
        question_id = request.POST.get('question_id')
        
        if question_id:
            quest_update_obj = Questions.objects.filter(id=question_id).update(text=question_text, media_url=media_url,
                                                                                media_type=media_type, hints=hints,
                                                                                flag=flag)
        else:
            quest_create_obj = Questions.objects.create(text=question_text, media_url=media_url,
                                                        media_type=media_type, hints=hints, flag=flag)
            
        res = {"message": "Question" + "updated" if question_id else "created" + "successfully"}
        return Response(res, status.HTTP_200_OK)
        
        
class ContentS3Upload(APIView):
    
    @staticmethod
    def post(request):
        file = request.FILES.get('media')
        media_for = request.POST.get('media_for')
        
        if not file:
            res = {"message": "No file found."}
            return Response(res, status.HTTP_400_BAD_REQUEST)
        if media_for == "choice":
            url = aws_upload_url(file, "images/choices-images/")
        elif media_for == "question":
            url = aws_upload_url(file, "images/question-images/")
        elif media_for == "question-hint":
            url = aws_upload_url(file, "images/question-descriptions/")

        if url:
            res = {"message": "Media uploaded successfully", "result": {"url": url}}
            return Response(res, status.HTTP_200_OK)
        else:
            res = {"message": "Something went wrong"}
            return Response(res, status.HTTP_500_INTERNAL_SERVER_ERROR)