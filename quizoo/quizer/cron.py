from .models import Quiz
from django.utils import timezone
from django.core.mail import send_mass_mail


def my_scheduled_job():
    print("Cron Job")
    li = Quiz.objects.filter(expired=False, end_time__lt=timezone.now(
    )).prefetch_related('usersgivingtest_set').select_related('admin')
    try:
        for z in li:
            # Set their expired=True
            print(z.id)
            if(z.email_result_creator == True):
                send_email_creator(z.admin.email)
            if(z.email_result_testtaker == True):
                x = z.usersgivingtest_set.all().select_related('user')
                send_email_testTakers(x)
            z.expired = True
            z.save()
    except Exception as e:
        print(e)
    print("Mail Service Completed")


def sendmail(mails):
    print("Coming to send mail")
    print(mails)
    send_mass_mail(mails, fail_silently=False)


def send_email_creator(mail):
    subject = "Quiz Result"
    sender_mail = "ctrlaltelitesih2020@gmail.com"
    body = "The test you conducted is over check the results at "+"url"
    sendmail([(subject, body, sender_mail, [mail])])


def send_email_testTakers(mails):
    subject = "Quiz Results"
    sender_mail = "ctrlaltelitesih2020@gmail.com"
    li = []
    for mail in mails:
        # Body consist of score of this student
        body = mail.user.username+" your Test Score is "+str(mail.score)
        li.append((subject, body, sender_mail, [mail.user.email]))
    sendmail(li)
