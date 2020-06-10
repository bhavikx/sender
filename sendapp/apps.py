from django.apps import AppConfig


class SendappConfig(AppConfig):
    name = 'sendapp'

    def ready(self):
    	import sendapp.signals