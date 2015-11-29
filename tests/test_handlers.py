# -*- coding: utf-8 -*-
from sms import base, exceptions, handlers

from unittest import TestCase


class NoSendMessageUrlHandler(handlers.SMSC):
    """
    Improperly configured sms handler
    """
    SEND_MESSAGE_URL = None


class NoGetSendMessagePostDataHandler(handlers.SMSC):
    """
    Improperly configured sms handler
    """

    #: emulate call base sms handler
    def get_send_message_post_data(self, request):
        return base.BaseSMSHandler.get_send_message_post_data(self, request)


class TestHandlers(TestCase):
    """
    Handlers test
    """

    def setUp(self):
        self.auth_credentials = {
            'user': 'user',
            'api-key': 'api-key'
        }

    def test_handler_improperly_configured(self):
        """
        there could be some handlers that won't work just as they have
        `gaps` inside interface they should implement
        """
        with self.assertRaises(exceptions.ImproperlyConfigured):
            NoSendMessageUrlHandler(self.auth_credentials)

    def test_handler_get_send_message_post_data_not_set(self):
        """
        No get_send_message_post_data had been set in given subclass
        """
        with self.assertRaises(NotImplementedError):
            handler = NoGetSendMessagePostDataHandler(self.auth_credentials)
            handler.send('test message', phone='127001')
