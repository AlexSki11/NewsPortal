import datetime

from celery import shared_task
import time
from .signals import send_email
from .models import Post, User
from django.utils import timezone

@shared_task
def create_post(post_id):
    post = Post.objects.get(pk=post_id)
    emails = []
    categories = post.post_category.all()
    for category in categories:
        emails.extend(User.objects.filter(subscriptions__category=category).values_list('email', flat=True))
        send_email(post, emails, category.name)
        emails.clear()

@shared_task
def share_news_monday():

    date = timezone.now() - datetime.timedelta(days=7)
    post_list = Post.objects.filter(data_create__gt=date)
    emails = []

    for post in post_list:
        categories = post.post_category.all()
        for category in categories:
            emails.extend(User.objects.filter(subscriptions__category=category).values_list('email', flat=True))
            send_email(post, emails, category.name)
            emails.clear()

