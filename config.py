from __future__ import annotations

import os
from typing import Optional

from pyhocon import ConfigFactory


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instance: Optional[Config] = None

    def __call__(self) -> Config:
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class Config(metaclass=SingletonMeta):
    def __init__(self):
        self.APP_CONFIG_PATH = os.getenv('APP_CONFIG_PATH', 'app.conf')

    def get_app_config(self):
        return ConfigFactory.parse_file(self.APP_CONFIG_PATH)
