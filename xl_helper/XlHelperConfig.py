from ConfigParser import RawConfigParser
from os.path import join, expanduser

class XlHelperConfig(object):

    config = None


    def __init__(self, config):
        assert config is not None
        self.config = config

    @staticmethod
    def load():
        defaults = {
            "username": "",
            "password": ""
        }
        config = RawConfigParser(defaults=defaults, allow_no_value=True)
        config.read([join(expanduser("~"), '.xl-helper')])
        XlHelperConfig.config = config



XlHelperConfig.load()