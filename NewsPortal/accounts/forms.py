from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

class SignUpForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        #Добавление пользователя в группу
        common_users = Group.objects.get(name="USERS")
        user.groups.add(common_users)

        #Отправка смс при регистрации нового пользователя
        subject = 'Добро пожаловать в наш интернет-магазин!'
        text = f'{user.username}, вы успешно зарегистрировались!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/products">сайте</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

        return user