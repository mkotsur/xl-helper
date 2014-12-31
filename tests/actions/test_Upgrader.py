import unittest

from os import path
from tests.util.TestingUtils import TestingUtils
from xl_helper.actions.Installer import Installer
from xl_helper.actions.Server import Server
from xl_helper.actions.Upgrader import Upgrader
from xl_helper.artifacts.server.RemoteServerDist import RemoteServerDist
from tests.util.TestWithTempDirs import TestWithTempDirs


class UpgraderTest(TestWithTempDirs):

    def setUp(self):
        self.upgrader = Upgrader(self.test_config)
        self.installer = Installer(self.test_config)
        self.temp_dir = self.create_temp_dir()

    def test_upgrade_in_place_from_remote_dist(self):
        home = self.installer.server(RemoteServerDist("4.5.1", self.test_config), target=self.temp_dir)
        self._assert_correct_installation(home, "4.5.1")
        self.upgrader.upgrade(home, RemoteServerDist("4.5.2", self.test_config))
        self._assert_correct_installation(home, "4.5.2")

    # def test_update_server(self):
    #     home_3 = self.installer.server(RemoteServerDist('3.9.2', self.test_config), target=self.temp_dir)
    #     self.installer.plugin('was', '3.9.0', home_3)
    #
    #     new_home = self.default_temp + "/new-ver"
    #     self.upgrader.upgrade(home_3, RemoteServerDist("4.5.2", self.test_config))
    #
    #     TestingUtils.assert_valid_server_installation(new_home)
    #
    #     assert path.isfile(path.join(new_home, 'plugins/file-plugin-4.5.2.jar'))
    #     assert not path.isfile(path.join(new_home, 'plugins/file-plugin-3.9.2.jar'))
    #     assert path.isfile(path.join(new_home, 'plugins/was-plugin-3.9.0.jar'))

    # Extra assertions

    def _assert_correct_installation(self, home, version):
        server = Server.from_config(self.test_config, home)
        TestingUtils.assert_valid_server_installation(home)
        self._assert_plugin_present(home, "file-plugin", version)

        server.start_and_wait()
        self.assertTrue(server.is_running())
        server.stop()

    def _assert_plugin_present(self, home, plugin, version):
        self.assertTrue(path.isfile(path.join(home, 'plugins/%s-%s.jar' % (plugin, version))))


if __name__ == '__main__':
    unittest.main()