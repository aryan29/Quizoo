from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list
# Create your models here.


class Quiz(models.Model):
    # User who created this quiz
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    quiz_name = models.CharField(max_length=50)  # Quiz Name
    start_time = models.DateTimeField()  # Quiz Start Time
    end_time = models.DateTimeField()  # Quiz End Time


class Questions(models.Model):
    # To which quiz this question belongs too
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)  # Question Text


class Options(models.Model):
    # This is an Option of which Question
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    option = models.CharField(max_length=100)  # Option Text


class CorrectOptions(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    option = models.CharField(max_length=100)


class UsersGivingTest(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.SmallIntegerField()
    questions_not_attempted = models.CharField(
        max_length=2000,
        verbose_name="question_list",
        validators=[validate_comma_separated_integer_list]
        
    )
