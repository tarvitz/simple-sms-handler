# -*- coding: utf-8 -*-
from . import base


class SMSC(base.BaseSMSHandler):
    """
    http://smsc.ru simple example handler
    """
    SEND_MESSAGE_URL = 'http://smsc.ru/some-api/message/'

    def get_send_message_post_data(self, request):
        return {
            'phone': request.phone,
            'message': request.message,
            'username': self.auth_credentials['username'],
            'api-key': self.auth_credentials['api-key']
        }


class SMSTraffic(base.BaseSMSHandler):
    """
    http://smstraffic.ru
    """
    SEND_MESSAGE_URL = 'http://smstraffic.ru/super-api/message/'

    def get_send_message_post_data(self, request):
        return {
            'Phone': request.phone,
            'Message': request.message,
            'Uid': self.auth_credentials['uid'],
            'ApiKey': self.auth_credentials['api-key'],
        }
