from __future__ import annotations

import os

from pyhocon import ConfigFactory


# from typing import Optional


class Singleton(object):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance


class Config(Singleton):
    def __init__(self):
        self.APP_CONFIG_PATH = os.getenv('APP_CONFIG_PATH', 'app.conf')
        self.app_conf = ConfigFactory.parse_file(self.APP_CONFIG_PATH)

    def get_app_config(self):
        return self.app_conf


if __name__ == '__main__':
    a = Config()
    b = Config()
    print(a is b)

'''
class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. I choose Metaclass
    """

    _instance: Optional[Config] = None

    def __call__(self) -> Config:
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class Config(metaclass=SingletonMeta):
    def __init__(self):
        self.APP_CONFIG_PATH = os.getenv('APP_CONFIG_PATH', 'app.conf')
        self.app_conf = ConfigFactory.parse_file(self.APP_CONFIG_PATH)
    def get_app_config(self):
        return self.app_conf

'''
