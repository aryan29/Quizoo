from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Questions, Quiz
from django.utils import timezone
from ckeditor.widgets import CKEditorWidget


class CreatingQuizForm(ModelForm):

    class Meta:
        model = Quiz
        fields = [
            'quiz_name',
            'start_time',
            'end_time'
        ]
        widgets = {
            'quiz_name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex:- Quiz Name"}),
            'start_time': forms.DateTimeInput(attrs={"class": "form-control", "placeholder": "Start Time", 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={"class": "form-control", "placeholder": "End Time", 'type': 'datetime-local'})
        }

    def clean(self):
        try:
            print("Coming to clean")
            cleaned_data = super(CreatingQuizForm, self).clean()
            start_time = cleaned_data.get("start_time")
            end_time = cleaned_data.get("end_time")
            print(start_time)
            print(end_time)
            try:
                if(start_time < timezone.now()):
                    self.add_error(
                        'start_time', 'Start time should be greater than current time')
                if(end_time < start_time):
                    self.add_error(
                        'end_time', 'End time should be greater than start time')
                return cleaned_data
            except Exception as e:
                print(e)
        except Exception as e:
            print("Raising exception", e)


class QuestionViewForm(forms.ModelForm):
    
    class Meta:
        model = Questions
        fields = ('question_text',)
