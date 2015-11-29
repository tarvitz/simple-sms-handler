from sms.registry import Registry

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SmsConfig(AppConfig):
    name = 'apps.sms'
    verbose_name = _("SMS Log module")

    def ready(self):
        """
        on app ready
        """
        registry = Registry()
        registry.register('apps.sms.handlers.MyProvider')
