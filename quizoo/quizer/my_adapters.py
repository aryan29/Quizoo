from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import render
class MySocialAccount(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        print("Coming to pre social login")
        u = sociallogin.user
        # if not u.email.split('@')[1] == "bitmesra.ac.in":
        #     raise ImmediateHttpResponse(render(None,'error.html'))