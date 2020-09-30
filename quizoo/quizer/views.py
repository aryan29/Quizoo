from datetime import datetime
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import CreatingQuizForm
from .models import Quiz,Questions,Options,CorrectOptions, UsersGivingTest
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from random import shuffle
from django.db.models import Q
from django.utils import timezone
import xlwt
# Create your views here.


@login_required(login_url='/accounts/login/')
def CreateQuizView(request):
    print(request.method)
    if(request.method=='POST'):
        form=CreatingQuizForm(request.POST)
        if(form.is_valid()):
            obj=form.save(commit=False)
            obj.admin=request.user
            obj.save()
            return redirect('/create')
        else:
            print("Getting Errors Dude")
            return render(request, 'create_quiz.html',{'form':form,'errors':form.errors})
    else:
        return render(request, 'create_quiz.html',{'form':CreatingQuizForm()})

# def CreateQuizEnpoint(request):
    
def ShowAllQuizToBeHeld(request):
    li=Quiz.objects.filter(admin=request.user,start_time__gt=timezone.now()) #Quiz hasnt started yet
    return render(request,'show_quiz.html',{"list":li})

@login_required(login_url='/accounts/login/')
@csrf_exempt
def EditQuiz(request,id):
    quiz=Quiz.objects.get(pk=id)
    #Quiz belongs to this user and it hasnt started yet

    if(quiz.admin==request.user and quiz.start_time>timezone.now()):
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
            
            return render(request,'edit_quiz.html',{"list":li,"name":quiz.quiz_name})
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
    print(quiz.start_time)
    print(timezone.now())
    print(quiz.start_time<timezone.now())
    if(request.method=="POST" and quiz.start_time<timezone.now() and quiz.end_time>timezone.now()):
        #If this quiz has started and hasnt ended than only we can make entry in db 
        #for user giving particular test
        print("Allowing user to give test")
        questions=cache.get(f'quiz{quiz}')
        if questions is None:
            print("Storing in cache")
            questions=list(quiz.questions_set.all())
            cache.set(
                f"quiz{quiz}",
                questions,
                60*60*3
            )
        #Setting all questions for particular quiz in cache for 3hours
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
        
        print((quiz.start_time.timestamp()))
        return render(request,'start-quiz.html',{"start":quiz.start_time.timestamp()})
        
@login_required(login_url='/accounts/login/')
def GetQuestions(request,id):
    quiz=Quiz.objects.get(pk=id)
    obj=UsersGivingTest.objects.filter(quiz=quiz,user=request.user)
    #Show 1 st question in question list
    if(obj.count()==0):
        return HttpResponse(400) #This person hasn't clicked on start test and is trying something unusual to start test
    else:
        obj=obj[0]
    st=obj.questions_not_attempted
    if(st=="" or quiz.end_time<timezone.now()):
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
            "options":opt,
            "end_time":quiz.end_time.timestamp()
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
    if(r1.sort()==r2.sort()): #If both are same
        score=1
    print("Score ",score)
    return score

@login_required(login_url='/accounts/login/')
def SeeCompletedQuiz(request):
    obj=Quiz.objects.filter(end_time__lt=timezone.now(),admin=request.user).order_by('-end_time')
    print(obj)
    return render(request,'completed_quiz.html',{"list":obj})
    #List of completed quizes
    pass

@login_required(login_url='/accounts/login/')
def SeeAnalytics(request,id):
    quiz=Quiz.objects.get(pk=id)
    if(quiz.admin==request.user):
        #He can view analytics for this quiz
        li=quiz.usersgivingtest_set.all()
        #List of all users who gave this quiz
        return render(request,'quiz_results.html',{"list":li})
        pass
    else:
        return HttpResponse(400)
    
@login_required(login_url='/accounts/login/')
def export_users_xls(request,id):
    quiz=Quiz.objects.get(pk=id)
    if(quiz.admin==request.user):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="users.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users')
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Userame', 'Email', 'Score']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()

        rows = quiz.usersgivingtest_set.all()
        
        print(rows)
        for x in rows:
            print(x.user.username)
            print(x.user.email)
            print(x.score)
        for row in rows:
            row_num += 1
            elem=[row.user.username,row.user.email,row.score]
            for i,x in enumerate(elem):
                ws.write(row_num, i,x,font_style)

        wb.save(response)
        return response


            
    
    
    
        
        
        
        
        
    
    

    
    
    
    
    
    
    
    
    
        