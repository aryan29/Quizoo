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
        widgets = {
            'quiz_name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex:- Quiz Name"}),
            'start_time': forms.DateTimeInput(attrs={"class": "form-control", "placeholder": "Start Time",'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={"class": "form-control", "placeholder": "End Time",'type': 'datetime-local'})
        }


