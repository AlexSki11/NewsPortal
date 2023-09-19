from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

class SignUpForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        common_users = Group.objects.get(name="USERS")
        user.groups.add(common_users)
        return user