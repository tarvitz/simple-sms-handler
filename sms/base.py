# -*- coding: utf-8 -*-
import requests
import logging
import json

from . import exceptions
from . import const

logger = logging.getLogger('sms.base')


class Request(object):
    """
    Simple sms request
    """

    def __init__(self, message, phone):
        self.message = message
        self.phone = phone


class BaseSMSHandler(object):
    """
    Base sms handler class
    """
    #: url there should go send message like request
    SEND_MESSAGE_URL = None
    #: field that should use as success/failure process identification
    MESSAGE_STATUS_FIELD = 'status'

    def __init__(self, auth_credentials=None):
        self.auth_credentials = auth_credentials or {}
        if self.SEND_MESSAGE_URL is None:
            raise exceptions.ImproperlyConfigured(
                "`SEND_MESSAGE_URL` is not set"
            )

    @staticmethod
    def log(level, payload):
        """
        store log information

        - INFO level means everything is fine
        - ERROR level means there had been a error while sms send request
            was trying to complete
        - CRITICAL level means there was internal server error or similar

        :param str level: log level
        :param dict payload: handler payload
        :rtype: None
        :return: None
        """

        log_level = getattr(logger, logging.getLevelName(level).lower(),
                            logger.info)
        log_level(json.dumps(payload))

    def process_response(self, request, response):
        """
        processes raw sms gate response and make it unified

        :param Request request: request
        :param requests.Response response: response
        :return: unified response
        """
        result = {
            'status': const.STATUS_ERROR,
            'phone': request.phone,
            'message': request.message
        }
        #: server is down or malformed data in response
        if response.headers.get('Content-Type') not in ('application/json',):
            result.update({
                'gate-payload': {'details': 'internal server error'}
            })
            self.log(logging.CRITICAL, result)
            return result
        else:
            payload = response.json()
            success_state = self.get_success_state(payload)
            logging_level = (
                success_state == const.STATUS_OK and logging.INFO or
                logging.ERROR
            )
            result.update({
                'status': success_state,
                'gate-payload': payload
            })
            self.log(logging_level, result)
            return result

    def get_send_message_post_data(self, request):
        """
        get send message data to post, each sms service could have
        its own data format to process

        :param Request request: request
        :rtype: dict
        :return: data to post
        :raises NotImplemented:
            - if you try to pass base get_send_message_post_data
        """
        raise NotImplementedError

    def get_send_message_headers(self):
        """
        get send message headers (simple ones)

        :rtype: dict
        :return: dict
        """
        return {}

    def get_success_state(self, payload):
        """
        get success state for given sms provider payload

        :param dict payload: sms provider response payload (json by origin)
        :rtype: str
        :return: success state
        """
        if payload.get(self.MESSAGE_STATUS_FIELD) == const.STATUS_OK:
            return const.STATUS_OK
        return const.STATUS_ERROR

    def send(self, message, phone, **attrs):
        """
        send message

        :param str phone: phone number where sms should go
        :param str message: message to send
        :param dict attrs: extra attributes
        :rtype: dict
        :return: response
        """
        request = Request(message, phone)
        response = requests.post(
            self.SEND_MESSAGE_URL,
            data=self.get_send_message_post_data(request),
            headers=self.get_send_message_headers()
        )
        return self.process_response(request, response)
