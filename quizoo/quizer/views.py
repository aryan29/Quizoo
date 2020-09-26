from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CreatingQuizForm
from .models import Quiz,Questions,Options,CorrectOptions, UsersGivingTest
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from random import shuffle
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

@login_required(login_url='/accounts/login/')
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
    
@login_required(login_url='/accounts/login/')
def QuizStart(request,id):
    quiz=Quiz.objects.get(pk=id)
    questions=list(Quiz.questions_set.all())
    questions=shuffle(questions)
    q=','.join([str(i) for i in questions])
    if(UsersGivingTest.objects.filter(quiz=quiz,user=request.user).count()==0):
        #If this user is not already giving this quiz create a new object
        UsersGivingTest.objects.create(
            quiz=quiz,
            user=request.user,
            score=0,
            questions_not_attempted=q
        )
        
@login_required(login_url='/accounts/login/')
def GetQuestions(request,id):
    quiz=Quiz.objects.get(pk=id)
    obj=UsersGivingTest.objects.filter(quiz=quiz,user=request.user)[0]
    #Show 1 st question in question list
    li=obj.questions_not_attempted.split(",")
    if(len(li)==0):
        return render(request,'end_quiz.html')
    if(request.method=="GET"):
        #person is just reloading the url
        display_question=li[0]
        return render(request,'question_view.html',{})
    elif(request.method=="POST"):
        #person is submitting the question
        #check for his response remove start ques from lst
        res=request.POST
        display_question=li[0]
        # increase score of this person if correct res
        
        new_li=li[1:]
        s=','.join([str(i) for i in new_li])
        obj.questions_not_attempted=s
        obj.save()
        #change not attempted questions in db for this person for this quiz
        return JsonResponse({
            
        })
        
        
        
        
        
    
    

    
    
    
    
    
    
    
    
    
        