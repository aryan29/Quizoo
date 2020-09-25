from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='/accounts/login/')
def CreateQuizView(request):
    return render(request, 'create_quiz.html')
