from django.test import SimpleTestCase
from django.urls import resolve,reverse
class TestUrls(SimpleTestCase):
    def test_login(self):
        self.assertEquals(reverse('login-view'),'/login/')
    def test_create_quiz(self):
        self.assertEquals(reverse('create-quiz'),'/create/')
    def test_check_valid_quiz_code(self):
        self.assertEquals(reverse('check-valid-quiz-code'),'/checkValid/')
    def test_show_quiz(self):
        self.assertEquals(reverse('list-quizes'),'/show/')
    
    
