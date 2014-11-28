import unittest

from os import path
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

        xld = Server.from_config(self.test_config, home)

        self.upgrader.upgrade(home, RemoteServerDist("4.5.2", self.test_config))
        self._assert_plugin_present(home, "file-plugin", "4.5.2")
        self._assert_starts_successfully(xld)


    def xtest_failed_upgrade(self):
        self.fail("Not implemented")

    # Extra assertions

    def _assert_starts_successfully(self, server):
        server.start_and_wait()
        self.assertTrue(server.is_running())
        server.stop()

    def _assert_plugin_present(self, home, plugin, version):
        # self._assert_valid_server_installation(home)
        self.assertTrue(path.isfile(path.join(home, 'plugins/%s-%s.jar' % (plugin, version))))

    def _assert_valid_server_installation(self, home):
        assert path.isfile(path.join(home, 'conf/deployit-license.lic'))
        assert path.isdir(path.join(home, 'bin'))
        assert path.isdir(path.join(home, 'lib'))
        assert path.isdir(path.join(home, 'ext'))

    def _assert_valid_cli_home(self, home):
        self.assertTrue(path.isdir(home))
        self.assertTrue(path.isfile(path.join(home, "bin", "cli.sh")))



if __name__ == '__main__':
    unittest.main()