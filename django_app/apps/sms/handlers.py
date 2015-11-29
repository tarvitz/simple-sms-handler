# -*- coding: utf-8 -*-
import logging
import json

from sms import base

from django.conf import settings
from django.apps import registry


class MyProvider(base.BaseSMSHandler):
    SEND_MESSAGE_URL = 'http://smsgate.blacklibrary.ru/sms/send-message/'

    def get_send_message_post_data(self, request):
        """
        What exactly we should send to send-message api url resource

        :param sms.base.Request request: simple sms send message request
        :rtype: dict
        :return: request data for sms send message api resource url in
            MyProvider format
        """
        return {
            'message': request.message,
            'phone': request.phone,
            'api_key': settings.MY_PROVIDER_API_KEY
        }


class DjangoSMSLogHandler(logging.Handler):
    """
    Django log handler for sms purpose
    """

    def __init__(self):
        super(DjangoSMSLogHandler, self).__init__()

    def emit(self, record):
        payload = json.loads(record.msg)
        payload.update({
            'level': record.levelno,
            'payload': json.dumps(payload.pop('gate-payload', '{}'))
        })
        self.create_log_entry(**payload)

    @staticmethod
    def create_log_entry(**payload):
        """
        create log entry

        :param dict payload: sms.Log fields to store
        :rtype: None
        :return: None
        """
        model_class = registry.apps.get_model('sms.Log')
        model_class.objects.create(**payload)
