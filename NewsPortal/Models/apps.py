from django.apps import AppConfig
from django.db.models.signals import m2m_changed

class ModelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Models'

   #Т.к. было дано задание сделать рассылку через celery, решил выключить сигнал
   # def ready(self):
    #    from . import signals
     #   m2m_changed.connect(signals.post_created)

