from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives

from .models import Post, User, Subscriptions, Category
@receiver(m2m_changed, sender=Post.post_category.through)
def post_created(sender, instance, action, **kwargs):
    if action == 'post_add':
        emails = []
        categories = sender.category.get_queryset()
        categories_names = []
        for category in categories:
            emails.extend(User.objects.filter(subscriptions__category=category).values_list('email', flat=True))
            categories_names.append(category.name)

        send_email(instance, emails, categories_names)
    else:
         return

def send_email(instance, emails, categories_names):
    subject = f"Новый пост в категории {','.join(categories_names)}"

    text_content = (
        f'Автор: {instance.get_author_str()}\n'
        f'Заголовок {instance.header}\n'
        f'Превью:\n {instance.preview()}\n'
        f'ссылка на пост http://127.0.0.1:8000{instance.get_absolute_url()}'
    )

    html_content = (
        f'Автор: {instance.get_author_str()}<br>'
        f'Заголовок {instance.header}<br><br>'
        f'Превью:<br> {instance.preview()}<br>'
        f'ссылка на пост <a href="http://127.0.0.1{instance.get_absolute_url()}">'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()