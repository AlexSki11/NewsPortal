import datetime
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from ...models import *
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

logger = logging.getLogger(__name__)



def my_job():

    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(data_create__gt=last_week)
    categories = Category.objects.all()
    emails = []

    for category in categories:
        emails.extend(User.objects.filter(subscriptions__category=category).values_list('email', flat=True))
        posts_send = posts.filter(post_category=category)
        if posts_send:
            send_email(emails,posts_send,category.name)
        emails = []



def send_email(emails,posts,category_name):
    print(category_name)
    subject = f'Новые посты за неделю в категории {category_name}'
    text_content = ''
    html_content = ''
    for post in posts:
        text_content += (
            f'Автор: {post.get_author_str()}\n'
            f'Заголовок {post.header}\n'
            f'Превью:\n {post.preview()}\n'
            f'ссылка на пост http://127.0.0.1:8000{post.get_absolute_url()}\n\n'
        )

        html_content += (
            f'Автор: {post.get_author_str()}<br>'
            f'Заголовок {post.header}<br><br>'
            f'Превью:<br> {post.preview()}<br>'
            f'ссылка на пост <a href="http://127.0.0.1{post.get_absolute_url()}<br><br>">'
        )

    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, 'text/html')
        print('ok')
        msg.send()



# The `close_old_connections` decorator ensures that database connections,
# that have become unusable or are obsolete, are closed before and after your
# job has run. You should use it to wrap any jobs that you schedule that access
# the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age`
    from the database.
    It helps to prevent the database from filling up with old historical
    records that are no longer useful.

    :param max_age: The maximum length of time to retain historical
                    job execution records. Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week=4, hour=18),  # Every friday 18 hour seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")