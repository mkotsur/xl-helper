from xl_helper.FileUtils import FileUtils
from xl_helper.XlHelperConfig import XlHelperConfig


class TestingUtils(object):

    @staticmethod
    def get_test_config(include_jenkins=False):

        config = XlHelperConfig.config
        config.read(FileUtils.to_absolute_path("tests/resources/.xl-helper.test-overrides"))

        if not include_jenkins:
            config.remove_section('jenkins')

        return config