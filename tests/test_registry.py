# -*- coding: utf-8 -*-
import responses
from contextlib import closing

from sms import const, exceptions
from sms.registry import get_handler, Registry
from unittest import TestCase


class WrongSMSHandler(object):
    """
    Here's wrong sms handler class
    """


class TestRegistry(TestCase):
    def setUp(self):
        self.attrs = {
            'auth_credentials': {
                'username': 'user',
                'api-key': 'api-key',
            }
        }
        registry = Registry()
        registry.register('sms.handlers.SMSC')
        with closing(open('tests/responses/success.json', 'r')) as json_file:
            self.post_success = json_file.read()

    @responses.activate
    def test_get_smsc_handler(self):
        """
        success message send test case
        """
        handler = get_handler('sms.handlers.SMSC', **self.attrs)
        responses.add(responses.RequestsMock.POST,
                      handler.SEND_MESSAGE_URL,
                      body=self.post_success, status=200,
                      content_type='application/json')
        response = handler.send(message='тестовое сообщение',
                                phone='79149009900')
        self.assertEqual(response['status'], const.STATUS_OK)

    def test_get_unregistered_handler(self):
        """
        unregistered handler get
        """
        with self.assertRaises(exceptions.RegistryException):
            get_handler('sms.handlers.SMSTraffic')

    def test_register_wrong_handler(self):
        """
        register wrong handler
        """
        registry = Registry()
        with self.assertRaises(TypeError):
            registry.register('tests.test_registry.WrongSMSHandler')
