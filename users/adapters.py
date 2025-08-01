from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse

class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter to disable sign-ups
    """
    def is_open_for_signup(self, request):
        """
        Disable sign-ups by returning False
        """
        return False

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom social account adapter to disable social logins
    """
    def is_open_for_signup(self, request, sociallogin):
        """
        Disable social sign-ups by returning False
        """
        return False
    
    def pre_social_login(self, request, sociallogin):
        """
        Redirect social login attempts to a disabled page
        """
        return redirect('dashboard:signup_disabled') 