from .models import Quiz 
from django.utils import timezone
from django.core.mail import send_mass_mail
def my_scheduled_job():
    #Get list of all quizes 
    #Expired=false and time > current time
    print("Cron Job")
    # li=Quiz.objects.filter(expired=False,end_time__lt=timezone.now()).prefetch_related('usersgivingtest_set').select_related('admin')
    # for z in li:
    #     #Set their expired=True
    #     if(z.email_result_creator==True):
    #         x=z.usersgivingtest_set.all().select_related('user')
    #         send_email_creator(z.admin.email,x)
    #     if(z.email_result_testtaker==True):
    #         x=z.usersgivingtest_set.all().select_related('user')
    #         send_email_testTakers(x)
    #     # z.expired=True
    #     # z.save()
    # print("Mail Service Completed")
    
def sendmail(mails):
    pass
    # send_mass_mail(mails, fail_silently=False)
def send_email_creator(mail):
    subject="Quiz Result"
    sender_mail="ctrlaltelitesih2020@gmail.com"
    body="The test you conducted is over check the results at "+"url"
    sendmail(((subject,sender_mail,mail.user.email,body),))
    
    #Body consist of score of all students and redirect link
    sendmail()
def send_email_testTakers(mails):
    subject="Quiz Results"
    sender_mail="ctrlaltelitesih2020@gmail.com"
    li=[]
    for mail in mails:
        #Body consist of score of this student
        body=mail.user.username+" your Test Score is "+mail.score
        li.append((subject,sender_mail,mail.user.email,body))
    print(tuple(li))
    sendmail(tuple(li))