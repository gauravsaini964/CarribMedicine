from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
)
from rest_framework_jwt.authentication import api_settings
from django.contrib.postgres.fields import JSONField, DateRangeField
import datetime
import time
from rest_framework_jwt.utils import jwt_encode_handler
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`.

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, email, password=None):
        """Create and return a `User` with an email, username and password."""

        if email is None:
            raise TypeError('Users must have an email address.')
        if password is None:
            raise TypeError('Users must have a password address.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_user_otp_based(self, phone):
        """Create and return a `User` with an email, username and password."""

        if phone is None:
            raise TypeError('Users must have an phone_no')

        user = self.model(phone_no=self.phone)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    # def login_with_password(self, email, password):
    #     pass
    
    # def login_with_otp(self, phone_no, otp):

    #     if otp is None:
    #         raise TypeError('Superusers must have a password.')
        
    #     if otp == self.modeluser.otp:


class User(AbstractBaseUser, PermissionsMixin):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(unique=True, max_length=254)
    phone_no = models.CharField(unique=True, null=True, max_length=20)
    is_phone_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    otp = models.IntegerField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    # @property
    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.email

    @property
    def fullname(self):
        fullname = self.first_name + ' ' + self.last_name
        return fullname
    
    @property
    def token(self):
        epoch_time = int(time.time())
        india_time = datetime.datetime.fromtimestamp(epoch_time)
        expiry_time = india_time + api_settings.JWT_EXPIRATION_DELTA
        payload = {
            'id': self.id,
            'exp': expiry_time,
            'iat': int(time.time()),
            'nbf': int(time.time()),
        }
        token = jwt_encode_handler(payload)
        return token
        
    class Meta:
        db_table = 'user'


class AuthKey(models.Model):

    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=50, null=False, blank=False)
    desc = models.CharField(null=True, max_length=100)
    starts_at = models.DateTimeField(null=False, blank=False)
    ends_at = models.DateTimeField(null=False, blank=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'auth_key'

    def __str__(self):
        return self.key


class Courses(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    icon_url = models.URLField(max_length=1000, null=True)
    iamge_url = models.URLField(max_length=1000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    flag = models.BooleanField(default=True)

    class Meta:
        db_table = 'courses'

    def __str__(self):
        return self.name


class Subjects(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    icon_url = models.URLField(max_length=1000, null=True)
    iamge_url = models.URLField(max_length=1000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    flag = models.BooleanField(default=True)

    class Meta:
        db_table = 'subjects'

    def __str__(self):
        return self.name


class CourseSubjects(models.Model):

    id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey("Courses", on_delete=models.CASCADE)
    subject_id = models.ForeignKey("Subjects", on_delete=models.CASCADE)
    flag = models.BooleanField(default=True)

    class Meta:
        db_table = 'course_subjects'
        unique_together = ('course_id', 'subject_id')


class Questions(models.Model):

    id = models.BigAutoField(primary_key=True)
    text = models.CharField(max_length=255)
    question_type = models.IntegerField(default=None, null=True)
    media_url = models.URLField(max_length=1000, null=True)
    media_type = models.IntegerField(default=None, null=True)
    hints = JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    flag = models.BooleanField(default=True)

    class Meta:
        db_table = 'questions'

    def __str__(self):
        return self.text


class Choices(models.Model):

    id = models.BigAutoField(primary_key=True)
    text = models.CharField(max_length=255)
    media_url = models.URLField(max_length=1000, null=True)
    media_type = models.IntegerField(default=None, null=True)
    choice_type = models.IntegerField(default=1, null=True)
    hints = JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'choices'

    def __str__(self):
        return self.text


class QuestionsSubject(models.Model):

    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey("Questions", on_delete=models.CASCADE)
    subject = models.ForeignKey("Subjects", on_delete=models.CASCADE)
    flag = models.BooleanField(default=True)

    class Meta:
        db_table = "questions_subject"


class QuestionsChoices(models.Model):

    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey("Questions", on_delete=models.CASCADE)
    choice = models.ForeignKey("Choices", on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    flag = models.BooleanField(default=True)

    class Meta:
        db_table = "questions_choices"


class Quiz(models.Model):
     
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    quiz_type = models.CharField(max_length=9)
    marks = models.FloatField(default=0.00)
    percentage = models.FloatField(default=0.00)
    total_questions = models.IntegerField(default=0)
    questions_attempted = models.IntegerField(default=0)
    correct_questions = models.IntegerField(default=0)
    incorrect_questions = models.IntegerField(default=0)
    is_complete = models.BooleanField(default=False)
    result_set = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    entity_id = models.IntegerField(default=None)
    entity_type = models.CharField(default=None, max_length=255)
    flag = models.IntegerField(default=True)

    class Meta:
        db_table = 'quiz'
        managed = True


class QuizQuestions(models.Model):

    id = models.BigAutoField(primary_key=True)
    quiz = models.ForeignKey('Quiz', on_delete=models.DO_NOTHING)
    question = models.ForeignKey('Questions', on_delete=models.DO_NOTHING)
    user_answer = models.ForeignKey("Choices", on_delete=models.DO_NOTHING, related_name='user_answer', null=True)
    correct_answer = models.ForeignKey("Choices", on_delete=models.DO_NOTHING, related_name='correct_answer', null=True)
    marks = models.FloatField(default=0.00)
    response_time = models.FloatField(default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    flag = models.IntegerField(default=True)

    class Meta:
        db_table = 'quiz_questions'
        managed = True


class UserSubjectScore(models.Model):

    id = models.BigAutoField(primary_key=True)
    subject = models.ForeignKey("Subjects", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    flag = models.IntegerField()

    class Meta:
        db_table = 'user_subject_score'

    def __str__(self):
        return self.id


class QuestionBank(models.Model):
    id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255)
    type = models.IntegerField()
    flag = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'question_bank'


class QuestionsQuestionBank(models.Model):
    id = models.BigAutoField(primary_key=True)
    question_bank = models.ForeignKey('QuestionBank', models.DO_NOTHING)
    question = models.ForeignKey('Questions', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'question_question_bank'


class Years(models.Model):

    id = models.BigAutoField(primary_key=True)
    year = models.DateField(auto_now=False, auto_now_add=False)
    academic_year_start = models.DateField(auto_now=False, auto_now_add=False)
    academic_year_end = models.DateField(auto_now=False, auto_now_add=False)

    class Meta:
        db_table = 'years'

    def __str__(self):
        return self.year


class PracticePapers(models.Model):

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    question_bank = models.ForeignKey('QuestionBank', models.DO_NOTHING)
    year = models.ForeignKey("Years", on_delete=models.CASCADE)
    time_limit = models.IntegerField()
    is_time_per_question = models.BooleanField(default=False)
    guidelines = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    flag = models.BooleanField(default=True)

    class Meta:
        db_table = 'practice_papers'

    def __str__(self):
        return self.name


class PaperSubject(models.Model):

    id = models.BigAutoField(primary_key=True)
    subject = models.ForeignKey("Subjects", on_delete=models.CASCADE)
    practice_paper = models.ForeignKey("PracticePapers", on_delete=models.CASCADE)
    flag = models.BooleanField(default=True)

    class Meta:
        db_table = 'paper_subjects'