# -*- coding: utf-8 -*
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Log(models.Model):
    STATUS_CHOICES = (
        ('ok', _('ok')),
        ('error', _('error')),
        ('pending', _('pending'))
    )
    STATUS_CHOICES_DICT = dict(STATUS_CHOICES)

    phone = models.CharField(_('phone'), max_length=32)
    status = models.CharField(_('status'), max_length=32,
                              choices=STATUS_CHOICES, default='pending')
    message = models.CharField(
        _('message'), max_length=128, help_text=_('message by origin')
    )
    payload = models.TextField(_('provider payload'), blank=True)
    level = models.PositiveIntegerField(
        _('level'), default=10, help_text=_("logger's level")
    )

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = _('SMS Log')
        verbose_name_plural = _('SMS logs')
