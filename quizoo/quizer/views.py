from django.shortcuts import render,redirect
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
    quiz=Quiz.objects.get(id=id)
    if(request.method=="POST"):
        print(quiz)
        questions=quiz.questions_set.all()
        print(questions)
        questions=list(questions)
        print(questions)
        shuffle(questions)
        
        q=','.join([str(i.id) for i in questions])
        print(q)
        try:
            if(UsersGivingTest.objects.filter(quiz=quiz,user=request.user).count()==0):
                #If this user is not already giving this quiz create a new object
                UsersGivingTest.objects.create(
                    quiz=quiz,
                    user=request.user,
                    score=0,
                    questions_not_attempted=q
                )
            return redirect(f'/quiz/start/{id}')
        except Exception as e:
            print(e)
    else:
        return render(request,'start-quiz.html')
        
@login_required(login_url='/accounts/login/')
def GetQuestions(request,id):
    quiz=Quiz.objects.get(pk=id)
    obj=UsersGivingTest.objects.filter(quiz=quiz,user=request.user)[0]
    #Show 1 st question in question list
    st=obj.questions_not_attempted
    if(st==""):
        return render(request,'end_quiz.html')
    li=st.split(",")
    print(len(li))
    print(li[0])
    if(request.method=="GET"):
        #person is just reloading the url
        display_question=Questions.objects.get(id=int(li[0]))
        
        opt=display_question.options_set.values_list("option",flat=True)
        return render(request,'question_view.html',{
            "question_text":display_question.question_text,
            "options":opt
        })
    elif(request.method=="POST"):
        #person is submitting the question
        #check for his response remove start ques from lst
        res=request.POST
        print(res)
        display_question=Questions.objects.get(id=int(li[0]))
        # increase score of this person if correct res
        x=checkResponse(res.getlist('response[]'),list(display_question.correctoptions_set.values_list("option",flat=True)))
        new_li=li[1:]
        s=','.join([str(i) for i in new_li])
        obj.questions_not_attempted=s
        obj.score+=x
        obj.save()
        #change not attempted questions in db for this person for this quiz
        if(len(new_li)>0):
            new_ques=Questions.objects.get(id=int(new_li[0]))
            new_opt=list(new_ques.options_set.values_list("option",flat=True))
            return JsonResponse({
                "question":new_ques.question_text,
                "options":new_opt
            })
        else:
            return HttpResponse(500)
def checkResponse(r1,r2):
    print("Coming to check reponses")
    print(r1) #User Response 
    print(r2) #Actual Response
    score=1
    for res in r2:
        if res not in r1: #If user didnt marked this reponse in his answers
            score=0
    print("Score ",score)
    return score

            
    
    
    
        
        
        
        
        
    
    

    
    
    
    
    
    
    
    
    
        