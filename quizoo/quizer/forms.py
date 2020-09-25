from django import forms
from django.forms import ModelForm
from .models import Quiz 
class CreatingQuizForm(ModelForm):
    class Meta:
        model=Quiz
        fields=[
            'quiz_name',
            'start_time',
            'end_time'
        ]

