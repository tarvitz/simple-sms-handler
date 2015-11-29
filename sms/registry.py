# -*- coding: utf-8 -*-
import importlib
from . import base, exceptions


class Registry(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Registry, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_storage'):
            self._storage = {}

    def register(self, name):
        """
        register handler into class

        :param str name: app.module.HandlerClass format string
        :rtype: None
        :return: None
        :raises TypeError:
            - if given class is not BaseSMSHandler subclass type
        """
        module_name, klass_name = name.rsplit('.', 1)
        module = importlib.import_module(module_name)
        handler_class = getattr(module, klass_name, None)

        if not issubclass(handler_class, base.BaseSMSHandler):
            raise TypeError(
                "`%s` classes are allowed only" % base.BaseSMSHandler.__name__
            )

        self._storage[name] = handler_class

    def get_handler(self, name, **attrs):
        """
        get handler instance

        :param str name: app.module.HandlerClass format string
        :param dict attrs: extra attributes
        :rtype: base.BaseSMSHandler
        :return: handler
        """
        if name not in self._storage:
            raise exceptions.RegistryException(
                "handler `%s` hadn't being registered" % name
            )
        handler_class = self._storage[name]
        return handler_class(**attrs)


def get_handler(name, **attrs):
    """
    gets handler within given name

    :param str name: handler's name
    :param dict attrs: extra attributes
    :rtype: base.BaseSMSHandler
    :return: handler
    """
    registry = Registry()
    return registry.get_handler(name, **attrs)
