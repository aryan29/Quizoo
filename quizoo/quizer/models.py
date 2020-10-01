from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list
# Create your models here.


class Quiz(models.Model):
    # User who created this quiz
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    #Quiz Settings
    quiz_name = models.CharField(max_length=50)  # Quiz Name
    quiz_instructions=models.CharField(max_length=1000,default="")
    start_time = models.DateTimeField()  # Quiz Start Time
    end_time = models.DateTimeField()  # Quiz End Time
    randomizer=models.BooleanField(default=True)
    one_question_per_page=models.BooleanField(default=True)
    resume_later=models.BooleanField(default=False)
    email_result_creator=models.BooleanField(default=False)
    email_result_testtaker=models.BooleanField(default=False)
    show_score_after_test=models.BooleanField(default=False)
    reveal_answers_after_test=models.BooleanField(default=False)
    view_after_test=models.BooleanField(default=False)
    strict_mode=models.BooleanField(default=False)
    camera_mode=models.BooleanField(default=False)
    record_responses=models.BooleanField(default=False)


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.SmallIntegerField()
    questions_not_attempted = models.CharField(
        max_length=2000,
        verbose_name="question_list",
        validators=[validate_comma_separated_integer_list]
        
    )

    
