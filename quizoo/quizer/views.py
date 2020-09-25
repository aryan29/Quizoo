from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CreatingQuizForm
from .models import Quiz
from django.http import HttpResponse
# Create your views here.


@login_required(login_url='/accounts/login/')
def CreateQuizView(request):
    if(request.method=='POST'):
        form=CreatingQuizForm(request.POST)
        if(form.is_valid()):
            print(form)
            obj=form.save(commit=False)
            obj.admin=request.user
            obj.save()
            return render(request, 'create_quiz.html',{'form':CreatingQuizForm()})
        else:
            print("Getting Errors Dude")
            return render(request, 'create_quiz.html',{'form':form,'errors':form.errors})
    else:
        return render(request, 'create_quiz.html',{'form':CreatingQuizForm()})

def ShowAllQuizToBeHeld(request):
    li=Quiz.objects.filter(admin=request.user)
    print(li)
    return render(request,'show_quiz.html',{"list":li})

def EditQuiz(request,id):
    quiz=Quiz.objects.get(pk=id)
    if(quiz.user==reques.user):
        #Get All questions of this quiz
        questions=quiz.questions_set.all()
        li=[]
        for q in questions:
            op=q.options_set.all()
            corr=q.correctoptions_set.all()
            di={
                "question":q,
                "options":op,
                "correct_options":corr
            }
            li.append(di)
        
        return render(request,'edit_quiz.html',{"list":li})
    else:
        return HttpResponse(400)
    #Check if this person can edit this quiz or not
    
    
    #Show all questions + options in this quiz
    
    #Show a button to add a question
    