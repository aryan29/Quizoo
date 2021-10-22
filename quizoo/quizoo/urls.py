"""quizoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static
from django.conf import settings
from quizer.views import CreateQuizView, ShowAllQuizToBeHeld, EditQuiz, QuizStart, GetQuestions, SeeCompletedQuiz, SeeAnalytics, export_users_xls, DeleteQuestion, GiveQuiz, CheckValid, QuizSettings, CompareResponses, HomePage, CheatingDetector, PrepareLogs
from django_otp.admin import OTPAdminSite

admin.site.__class__ = OTPAdminSite
urlpatterns = [
    path('', HomePage, name='redirect'),
    path('helloadmin/', admin.site.urls,name='admin-panel'),
    path('accounts/', include('allauth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('login/', LoginView.as_view(), name='login-view'),
    path('create/', CreateQuizView, name='create-quiz'),
    path('checkValid/', CheckValid, name='check-valid-quiz-code'),
    path('show/', ShowAllQuizToBeHeld, name='list-quizes'),
    path('edit/<int:id>/', EditQuiz, name='edit-quiz'),
    path('settings/<int:id>/', QuizSettings, name='quiz-settings'),
    path('quiz/<int:id>/', QuizStart, name='quiz-start'),
    path('give-quiz/', GiveQuiz, name='give-quiz'),
    path('quiz/start/<int:id>', GetQuestions, name='get-questions'),
    path('completed/', SeeCompletedQuiz, name='completed-quizes'),
    path('analytics/<int:id>/', SeeAnalytics, name='analytics'),
    path('compareRes/<int:id>/', CompareResponses, name='compare-responses'),
    path('logs/<int:id>/', PrepareLogs, name='prepare-logs'),
    path('regular-checks/', CheatingDetector, name='cheating-detector'),
    path('analytics/download/<int:id>/',
         export_users_xls, name='download-excel-sheet'),
    path('delete/<int:id>/', DeleteQuestion, name='deleting question')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
