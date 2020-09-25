from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Quiz(models.Model):
    admin=models.OneToOneField(User,on_delete=models.CASCADE) #User who created this quiz
    quiz_name=models.CharField(max_length=50) #Quiz Name
    start_time = models.DateTimeField() #Quiz Start Time
    end_time=models.DateTimeField() #Quiz End Time

class Questions(models.Model):
    quiz=ForeignKey(Quiz,on_delete=models.CASCADE) # To which quiz this question belongs too
    question_text=models.CharField(max_length=500) #Question Text

class Options(models.Model):
    question=models.ForeignKey(Questions,on_delete=models.CASCADE) #This is an Option of which Question
    option=models.CharField(max_length=100) #Option Text

class CorrectOptions(models.Model):
    question=models.ForeignKey(Questions,on_delete=models.CASCADE)
    option=models.CharField(max_length=100)

