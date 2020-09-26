from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CreatingQuizForm
from .models import Quiz,Questions,Options,CorrectOptions
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
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

@csrf_exempt
def EditQuiz(request,id):
    quiz=Quiz.objects.get(pk=id)
    if(quiz.admin==request.user):
        #Get All questions of this quiz
        if(request.method=="GET"):
            questions=quiz.questions_set.all()
            print(questions)
            li=[]
            for q in questions:
                op=q.options_set.all()
                corr=q.correctoptions_set.all()
                print(op)
                print(corr)
                di={
                    "question":q,
                    "options":op,
                    "correct_options":corr
                }
                li.append(di)
            
            return render(request,'edit_quiz.html',{"list":li})
        elif(request.method=="POST"):
            data=request.POST
            print(data)
            print(data['question_text'])
            print(data.getlist('options[]'))
            
            #Add entry into db from post data
            #and return the response to append it if added in db successfully
            try:
                q=Questions.objects.create(
                    question_text=data['question_text'],
                    quiz=quiz
                    )
                for option in data.getlist('options[]'):
                    Options.objects.create(
                        option=option,
                        question=q
                    )
                for correct_option in data.getlist('correct_options[]'):
                    CorrectOptions.objects.create(
                    option=correct_option,
                        question=q
                    )
                return HttpResponse(200)
            except Exception as e:
                print(e)
                return HttpResponse(500)
            
                
            
            
    else:
        return HttpResponse(400)
    #Check if this person can edit this quiz or not
    
    
    #Show all questions + options in this quiz
    
    #Show a button to add a question
    