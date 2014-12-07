from os import path
from xl_helper.FileUtils import FileUtils
from xl_helper.XlHelperConfig import XlHelperConfig


class TestingUtils(object):

    @staticmethod
    def get_test_config(include_jenkins=False):

        config = XlHelperConfig.load()

        if not include_jenkins:
            config.remove_section('jenkins')

        return config

    @staticmethod
    def get_test_resource(resource):
        FileUtils.to_absolute_path("resources/%s" % resource)

    @staticmethod
    def assert_valid_server_installation(home):
        assert path.isfile(path.join(home, 'conf/deployit-license.lic'))
        assert path.isdir(path.join(home, 'bin'))
        assert path.isdir(path.join(home, 'lib'))
        assert path.isdir(path.join(home, 'ext'))

    @staticmethod
    def assert_valid_cli_home(home):
        assert path.isdir(home)
        assert path.isfile(path.join(home, "bin", "cli.sh"))




