from django.test import TestCase,Client
from django.contrib.auth.models import User
from ..models import Quiz, Questions, Options, CorrectOptions, TestLogs, UsersGivingTest, RecordedResponses
from django.urls import resolve,reverse
from django.utils import timezone


class TestViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user=User.objects.create(username='testuser')

        # Making one quiz
        cls.quiz=Quiz.objects.create(admin=cls.user,quiz_name="anything",start_time=timezone.now() ,end_time=timezone.now() )


        # Adding some questions and options to this quiz


        # Making a deafault userGivingTest


    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)
        self.home=reverse('redirect')
        self.create_quiz=reverse('create-quiz')
        self.give_quiz=reverse('give-quiz')
        self.show_quiz=reverse('list-quizes')

    def test_home_page(self):
        res=self.client.get(self.home)
        self.assertEqual(res.status_code,200)
        self.assertTemplateUsed(res,'base.html')

    def test_give_quiz_page(self):
        res = self.client.get(self.give_quiz)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'give_quiz.html')

    def test_show_quiz(self):
        res=self.client.get(self.show_quiz)
        self.assertEqual(res.status_code,200)
        self.assertTemplateUsed(res,'show_quiz.html')

    def test_create_quiz(self):
        res=self.client.get(self.create_quiz)
        self.assertEqual(res.status_code,200)
        self.assertTemplateUsed(res,'create_quiz.html')

    def test_valid_quiz_code(self):
        res=self.client.post(reverse('check-valid-quiz-code'),{
            "quiz_no":self.quiz.id
        })
        self.assertEqual(res.status_code, 200)

    
