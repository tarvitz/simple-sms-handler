# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import responses

from django.test import TestCase
from sms.registry import get_handler
from django.utils.text import force_text

from . import models


class LoggingTest(TestCase):
    """
    This test case use fake (but still real) api placed on
    http://smsgate.blacklibrary.ru/

    If there's no smsgate, use responses to apply mock payload data instead
    using real one
    """
    def setUp(self):
        self.post_success = json.dumps({
            'phone': '79149009900',
            'status': 'ok'
        })
        self.post_failure = json.dumps({
            "details": {"phone": ["Enter a valid value."]},
            "phone": None, "status": "error"
        })

    # @responses.activate
    def test_on_message_send(self):
        """
        sends message
        """
        count = models.Log.objects.count()
        handler = get_handler('apps.sms.handlers.MyProvider')
        #: fake response
        responses.add(responses.RequestsMock.POST,
                      handler.SEND_MESSAGE_URL,
                      body=self.post_success, status=200,
                      content_type='application/json')

        handler.send(message='сообщение', phone='79149009900')
        self.assertEqual(count + 1, models.Log.objects.count())

        log = models.Log.objects.latest('pk')
        self.assertEqual(log.message, 'сообщение')
        self.assertEqual(log.phone, '79149009900')
        self.assertEqual(
            log.status, force_text(models.Log.STATUS_CHOICES_DICT['ok'])
        )

    # @responses.activate
    def test_on_message_send_failure_params(self):
        """
        sends message with wrong params so sms gate should return an error
        """
        count = models.Log.objects.count()
        handler = get_handler('apps.sms.handlers.MyProvider')

        #: fake response
        responses.add(responses.RequestsMock.POST,
                      handler.SEND_MESSAGE_URL,
                      body=self.post_failure, status=400,
                      content_type='application/json')

        handler.send(message='сообщение', phone='error phone')
        self.assertEqual(count + 1, models.Log.objects.count())

        log = models.Log.objects.latest('pk')
        self.assertEqual(log.message, 'сообщение')
        self.assertEqual(log.phone, 'error phone')
        self.assertEqual(
            log.status, force_text(models.Log.STATUS_CHOICES_DICT['error'])
        )
