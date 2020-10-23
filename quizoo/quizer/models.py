from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list
from django.forms.fields import DateTimeField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class Quiz(models.Model):
    # User who created this quiz
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    # Quiz Settings
    quiz_name = models.CharField(max_length=50)  # Quiz Name
    quiz_instructions = models.CharField(max_length=1000, default="")
    start_time = models.DateTimeField()  # Quiz Start Time
    end_time = models.DateTimeField()  # Quiz End Time
    randomizer = models.BooleanField(default=True)  # Done
    one_question_per_page = models.BooleanField(default=True)  # Not Done
    resume_later = models.BooleanField(default=False)  # Useless
    email_result_creator = models.BooleanField(default=False)  # Done
    email_result_testtaker = models.BooleanField(default=False)  # Done
    show_score_after_test = models.BooleanField(default=False)  # Done
    reveal_answers_after_test = models.BooleanField(default=False)  # Not Done
    view_after_test = models.BooleanField(default=False)  # Not Done
    strict_mode = models.BooleanField(default=False)  # Done
    camera_mode = models.BooleanField(default=False)  # Not Done
    record_responses = models.BooleanField(default=False)  # Done
    # Whether quiz is over or not cron will detect quiz is over and send email to the users required if needed
    expired = models.BooleanField(default=False)  # Done


class Questions(models.Model):
    # To which quiz this question belongs too
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = RichTextUploadingField()  # Question Text


class Options(models.Model):
    # This is an Option of which Question
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    option = RichTextUploadingField()  # Option Text


class CorrectOptions(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    option = RichTextUploadingField()


class UsersGivingTest(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.SmallIntegerField()
    questions_not_attempted = models.CharField(
        max_length=2000,
        verbose_name="question_list",
        validators=[validate_comma_separated_integer_list]

    )


class RecordedResponses(models.Model):
    whom = models.ForeignKey(UsersGivingTest, on_delete=models.CASCADE)
    question_num = models.SmallIntegerField()
    time = models.DateTimeField(auto_now_add=True)
    responses = models.CharField(
        max_length=2000,
    )


class TestLogs(models.Model):
    whom = models.ForeignKey(UsersGivingTest, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=100)
    img = models.ImageField(upload_to='logs')
