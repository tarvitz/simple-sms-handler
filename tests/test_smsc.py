# -*- coding: utf-8 -*-
import responses

from sms import handlers, const
from contextlib import closing
from unittest import TestCase


class TestSMSC(TestCase):
    def setUp(self):
        self.auth_credentials = {
            'username': 'user',
            'api-key': 'api-key',
        }
        self.handler = handlers.SMSC(self.auth_credentials)

        with closing(open('tests/responses/success.json', 'r')) as json_file:
            self.post_success = json_file.read()
        with closing(open('tests/responses/failure_wrong_params.json',
                          'r')) as json_file:
            self.post_wrong_params = json_file.read()
        with closing(open('tests/responses/failure_cant_send.json',
                          'r')) as json_file:
            self.post_cant_send = json_file.read()

    @responses.activate
    def test_message_send(self):
        """
        success message send test case
        """
        responses.add(responses.RequestsMock.POST,
                      self.handler.SEND_MESSAGE_URL,
                      body=self.post_success, status=200,
                      content_type='application/json')
        response = self.handler.send(message='тестовое сообщение',
                                     phone='79149009900')
        self.assertEqual(response['status'], const.STATUS_OK)

    @responses.activate
    def test_message_send_failure(self):
        """
        message with wrong request params
        """
        responses.add(responses.RequestsMock.POST,
                      self.handler.SEND_MESSAGE_URL,
                      body=self.post_wrong_params, status=400,
                      content_type='application/json')
        response = self.handler.send(message='тестовое сообщение',
                                     phone='не правильный телефон')
        self.assertEqual(response['status'], const.STATUS_ERROR)

    @responses.activate
    def test_message_send_failure_cant_send(self):
        """
        message that have not been sent to addressee
        """
        responses.add(responses.RequestsMock.POST,
                      self.handler.SEND_MESSAGE_URL,
                      body=self.post_wrong_params, status=200,
                      content_type='application/json')
        response = self.handler.send(message='тестовое сообщение',
                                     phone='79149009900')
        self.assertEqual(response['status'], const.STATUS_ERROR)

    @responses.activate
    def test_message_send_internal_server_error(self):
        """
        server could fail (get down or just start to give response formats
        different from application/json
        """
        responses.add(responses.RequestsMock.POST,
                      self.handler.SEND_MESSAGE_URL,
                      body="internal server error", status=500,
                      content_type='text/html')
        response = self.handler.send(message='тестовое сообщение',
                                     phone='79149009900')
        self.assertEqual(response['status'], const.STATUS_ERROR)
