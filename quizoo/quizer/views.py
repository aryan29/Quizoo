
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CreatingQuizForm, QuestionViewForm
from .models import Quiz, Questions, Options, CorrectOptions, TestLogs, UsersGivingTest, RecordedResponses
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from random import shuffle
from django.db.models import Q
from django.utils import timezone
import xlwt
import json
import base64
from django.core.files.base import ContentFile
from django.db.models import Avg


# Create your views here.
@login_required(login_url='/accounts/login/')
def HomePage(request):
    return render(request, 'base.html')


@login_required(login_url='/accounts/login/')
def GiveQuiz(request):
    return render(request, 'give_quiz.html')


@login_required(login_url='/accounts/login/')
def CheckValid(request):
    if(request.method == 'POST'):
        try:
            data = int(request.POST['quiz_no'])
            if(Quiz.objects.filter(pk=data).count() > 0):
                return HttpResponse(200)
            else:
                return HttpResponse(400)
        except Exception as e:
            print(e)
            return HttpResponse(400)
    else:
        return HttpResponse(400)


@login_required(login_url='/accounts/login/')
def CreateQuizView(request):

    # print(request.method)
    if(request.method == 'POST'):
        print(request.POST)
        form = CreatingQuizForm(request.POST)
        print(form.is_valid())
        if(form.is_valid()):
            obj = form.save(commit=False)
            obj.admin = request.user
            obj.save()
            return HttpResponse(200)
        else:
            print("Getting Errors Dude", form.errors)
            return JsonResponse({"error": form.errors.as_text()})
    else:
        return render(request, 'create_quiz.html', {'form': CreatingQuizForm()})

# def CreateQuizEnpoint(request):


@login_required(login_url='/accounts/login/')
def ShowAllQuizToBeHeld(request):
    # Quiz hasnt started yet
    li = Quiz.objects.filter(admin=request.user, start_time__gt=timezone.now())
    return render(request, 'show_quiz.html', {"list": li})


@login_required(login_url='/accounts/login/')
def QuizSettings(request, id):
    quiz = Quiz.objects.get(pk=id)
    if(quiz.admin == request.user):
        if(request.method == 'GET'):
            return render(request, 'settings.html', {"quiz": quiz, "start": quiz.start_time, "end": quiz.end_time})
        elif(request.method == 'POST'):
            try:
                print(request.POST)
                ne = request.POST.getlist("list[]")
                quiz.quiz_instructions = ne[11]
                quiz.start_time = ne[12]
                quiz.end_time = ne[13]
                ne = [True if x == 'true' else False for x in ne]
                print(ne)
                quiz.randomizer = ne[0]
                quiz.one_question_per_page = ne[1]
                quiz.resume_later = ne[2]
                quiz.email_result_creator = ne[3]
                quiz.email_result_testtaker = ne[4]
                quiz.show_score_after_test = ne[5]
                quiz.reveal_answers_after_test = ne[6]
                quiz.view_after_test = ne[7]
                quiz.strict_mode = ne[8]
                quiz.camera_mode = ne[9]
                quiz.record_responses = ne[10]
                quiz.save()
                print("Done new settings saved")
            # Update Settings for this quiz
                return HttpResponse(200)
            except Exception as e:
                print(e)
                return HttpResponse(400)


@csrf_exempt
@login_required(login_url='/accounts/login/')
def EditQuiz(request, id):
    quiz = Quiz.objects.select_related('admin').get(pk=id)
    # Quiz belongs to this user and it hasnt started yet

    if(quiz.admin == request.user and quiz.start_time > timezone.now()):
        # Get All questions of this quiz
        if(request.method == "GET"):
            questions = quiz.questions_set.prefetch_related(
                "options_set", "correctoptions_set").all()
            # print(questions)
            li = []
            for q in questions:
                op = q.options_set.all()
                corr = q.correctoptions_set.all()
                # print(op)
                # print(corr)
                di = {
                    "question": q,
                    "options": op,
                    "correct_options": corr
                }
                li.append(di)

            form = QuestionViewForm()
            return render(request, 'edit_quiz.html', {"list": li, "name": quiz.quiz_name, "id": quiz.id, "form": form})
        elif(request.method == "POST"):
            data = request.POST
            print(data)
            print(data['question_text'])
            print(data.getlist('options[]'))

            # Add entry into db from post data
            # and return the response to append it if added in db successfully
            try:
                form = QuestionViewForm(data)
                print(form)
                if(form.is_valid()):
                    q = form.save(commit=False)
                    q.quiz = quiz
                    q.save()
                    print(q)
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
                else:
                    return HttpResponse(500)

            except Exception as e:
                print("Exception")
                print(e)
                return HttpResponse(500)
    else:
        return HttpResponse(400)


@login_required(login_url='/accounts/login/')
def QuizStart(request, id):
    quiz = Quiz.objects.get(id=id)
    print(quiz.start_time)
    print(timezone.now())
    print(quiz.start_time < timezone.now())
    if(request.method == "POST" and quiz.start_time < timezone.now() and quiz.end_time > timezone.now()):
        # If this quiz has started and hasnt ended than only we can make entry in db
        # for user giving particular test
        print("Allowing user to give test")
        # Setting all questions for particular quiz in cache for 3hours
        questions = cache.get(f'quiz{quiz}')
        if questions is None:
            print("Storing in cache")
            questions = list(quiz.questions_set.all())
            cache.set(
                f"quiz{quiz}",
                questions,
                60*60*3
            )

        # If randomizer is on shuffle questions
        if(quiz.randomizer):
            shuffle(questions)

        q = ','.join([str(i.id) for i in questions])
        print(q)
        try:
            if(UsersGivingTest.objects.filter(quiz=quiz, user=request.user).count() == 0):
                # If this user is not already giving this quiz create a new object
                UsersGivingTest.objects.create(
                    quiz=quiz,
                    user=request.user,
                    score=0,
                    questions_not_attempted=q
                )
            return HttpResponse(200)
        except Exception as e:
            print(e)
            return HttpResponse(400)
    elif(request.method == 'POST'):
        return HttpResponse(400)
    else:
        print((quiz.start_time.timestamp()))
        return render(request, 'start-quiz.html', {"quiz": quiz, "start": quiz.start_time.timestamp(), "end":  quiz.end_time.timestamp(), "instructions": quiz.quiz_instructions})


@login_required(login_url='/accounts/login/')
def GetQuestions(request, id):
    quiz = Quiz.objects.get(pk=id)
    obj = UsersGivingTest.objects.filter(quiz=quiz, user=request.user)
    # Show 1 st question in question list
    if(obj.count() == 0):
        # This person hasn't clicked on start test and is trying something unusual to start test
        return HttpResponse(400)
    else:
        obj = obj[0]
    st = obj.questions_not_attempted
    score = -1
    if(quiz.show_score_after_test):
        score = obj.score

    if(st == "" or quiz.end_time < timezone.now()):
        if(score != -1):
            return render(request, 'end_quiz.html', {"score": score, "show": True})
        else:
            return render(request, 'end_quiz.html', {"score": score, "show": False})

    li = st.split(",")
    if(request.method == "GET"):
        # person is just reloading the url show topmost question in list
        display_question = Questions.objects.get(id=int(li[0]))

        opt = display_question.options_set.values("id", "option")
        print(opt)
        return render(request, 'question_view.html', {
            "quiz": quiz,
            "question_text": display_question.question_text,
            "options": opt,
            "end_time": quiz.end_time.timestamp()
        })
    elif(request.method == "POST"):
        # person is submitting the question
        # check for his response remove start ques from list
        res = request.POST
        print("Here we are")
        display_question = Questions.objects.get(id=int(li[0]))
        # increase score of this person if correct res
        # user_res = [int(x) for x in res.getlist('response[]')]
        user_res = res.getlist('response[]')
        zz = list(Options.objects.filter(
            pk__in=user_res).values_list("option", flat=True))
        x = checkResponse(zz, list(
            display_question.correctoptions_set.values_list("option", flat=True)))
        RecordedResponses.objects.create(
            whom=obj,
            question_num=int(li[0]),
            responses=zz
        )
        print("Done till here")
        new_li = li[1:]
        s = ','.join([str(i) for i in new_li])
        obj.questions_not_attempted = s
        obj.score += x
        obj.save()
        # change not attempted questions in db for this person for this quiz
        if(len(new_li) > 0):
            new_ques = Questions.objects.get(id=int(new_li[0]))
            new_opt = list(
                new_ques.options_set.values("id", "option"))
            print(new_opt)
            return JsonResponse({
                "question": new_ques.question_text,
                "options": new_opt
            })
        else:
            return HttpResponse(500)


@login_required(login_url='/accounts/login/')
def DeleteQuestion(request, id):
    print(request)
    if(request.method == 'DELETE'):
        # Delete this question from database
        print("donw")
        Questions.objects.filter(pk=id).delete()
        return HttpResponse(200)
    else:
        return HttpResponse(400)


def checkResponse(r1, r2):
    print("Coming to check reponses")
    print(r1)  # User Response
    print(r2)  # Actual Response
    score = 0
    r1.sort()
    r2.sort()
    if(r1 == r2):  # If both are same
        score = 1
    print("Score ", score)
    # print("Score checked")
    return score


@login_required(login_url='/accounts/login/')
def SeeCompletedQuiz(request):
    obj = Quiz.objects.filter(
        end_time__lt=timezone.now(), admin=request.user).order_by('-end_time')
    return render(request, 'completed_quiz.html', {"list": obj})
    # List of completed quizes


@login_required(login_url='/accounts/login/')
def SeeAnalytics(request, id):
    quiz = Quiz.objects.get(pk=id)
    if(quiz.admin == request.user):
        # He can view analytics for this quiz

        if(quiz.record_responses):
            li = quiz.usersgivingtest_set.all()
            return render(request, 'quiz_results.html', {"list": li, "id": id, "showRes": True})
        else:
            li = quiz.usersgivingtest_set.all()
            return render(request, 'quiz_results.html', {"list": li, "id": id, "showRes": False})
    else:
        return HttpResponse(400)


@login_required(login_url='/accounts/login/')
def CompareResponses(request, id):
    obj = UsersGivingTest.objects.select_related('quiz').get(pk=id)
    r1 = list(obj.recordedresponses_set.values_list(
        "responses", flat=True).order_by('question_num'))
    # print(r1)
    # r2 = obj.quiz.correctoptions_set.all()
    # Get Quiz Name
    # From that get a list of questions in that quiz
    # From that get a list of correct responses
    quiz = obj.quiz
    # Only 2 db hit because  prefetching all correctoptions_set
    li = quiz.questions_set.prefetch_related('correctoptions_set')
    q = []
    r2 = []
    for question in li:
        q.append(question.question_text)
        z = [x.option for x in question.correctoptions_set.all()]
        r2.append(z)

    # print(q)
    # print(r1)
    # print(r2)

    return render(request, 'compare_res.html', {"questions": q, "user_res": r1, "correct_res": r2})


@login_required(login_url='/accounts/login/')
def export_users_xls(request, id):
    quiz = Quiz.objects.get(pk=id)
    if(quiz.admin == request.user):
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
            elem = [row.user.username, row.user.email, row.score]
            for i, x in enumerate(elem):
                ws.write(row_num, i, x, font_style)

        wb.save(response)
        return response


@login_required(login_url='/accounts/login/')
def CheatingDetector(request):
    data = request.POST
    # print(data)
    # Make an object of cheating attempt by this user
    user = request.user
    obj = UsersGivingTest.objects.filter(
        quiz__id=data['id'], user=user)[0]
    # # Save Image of this User Under his UsersGivingTest folder
    try:
        img_data = data['imgBase64']
        format, imgstr = img_data.split(';base64,')
        ext = format.split('/')[-1]
        file_name = "Cheat"+str(obj.id)+"."+ext
        file = ContentFile(base64.b64decode(imgstr), name=file_name)
    except:
        file = "#"  # No file attached
    print("Cheating detected by "+user.username+"in quiz" +
          data['id']+" at time "+str(timezone.now()))
    try:
        TestLogs.objects.create(
            whom=obj,
            type=data["type"],
            img=file,
        )
    except Exception as e:
        print(e)
        return HttpResponse(500)

    return HttpResponse(200)


@login_required(login_url='/accounts/login/')
def PrepareLogs(request, id):
    logs = TestLogs.objects.filter(
        whom__id=id).order_by('time')
    user = UsersGivingTest.objects.select_related(
        'quiz').select_related('user').get(id=id)
    # get avg of all users giving this quiz
    quiz = user.quiz
    avg_score = quiz.usersgivingtest_set.aggregate(Avg('score'))
    score = user.score
    res = user.recordedresponses_set.values_list(
        "time", flat=True).order_by('time')
    print(avg_score)
    if(len(res) != 0):
        complete_time = res[len(res)-1]-quiz.start_time
    else:
        complete_time = 0
    return render(request, 'log_page.html', {"name": user.user.username, "cheat_logs": logs, "score": score, "avg_score": avg_score['score__avg'], "res_logs": res, "complete_time": complete_time})
