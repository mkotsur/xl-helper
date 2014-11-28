import thread

from xl_helper.Utils import Utils
from xl_helper.actions.Installer import Installer
from xl_helper.actions.Server import Server
from xl_helper.artifacts.server.RemoteServerDist import RemoteServerDist
from tests.util.TestWithTempDirs import TestWithTempDirs


class ServerTest(TestWithTempDirs):

    def setUp(self):
        self.installer = Installer(self.test_config)
        temp_dir = self.create_temp_dir()

        home = self.installer.server(RemoteServerDist('4.0.0', self.test_config), temp_dir)
        self.server = Server.from_config(home, self.test_config)

    def tearDown(self):
        self.server.stop_and_wait()

    def test_operations(self):
        assert not self.server.is_running()
        assert self.server.is_stopped()

        self.server.start_and_wait()
        assert not self.server.is_running()  # still starting
        Utils.wait_until(self.server.is_running, tick=True)
        assert not self.server.is_stopped()  # has started starting

        thread.start_new_thread(self.server.restart, ())
        Utils.wait_until(self.server.is_stopped, tick=True)  # first should stop
        Utils.wait_until(self.server.is_running, tick=True)  # then should run

        self.server.stop_and_wait()
        assert not self.server.is_running()


