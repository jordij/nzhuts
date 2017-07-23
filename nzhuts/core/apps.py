from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'nzhuts.core'

    def ready(self):
        """
            Override this to put in:
                Help system checks
                Help signal registration
        """
        from . import signals
