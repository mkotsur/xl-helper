from os import path

from tests.util.TestWithTempDirs import TestWithTempDirs
from tests.util.TestingUtils import TestingUtils
from xl_helper.artifacts.server.RemoteServerDist import RemoteServerDist
import unittest


class RemoteServerDistTest(TestWithTempDirs):

    test_config_with_jenkins = TestingUtils.get_test_config(include_jenkins=True)

    def setUp(self):
        self.dist = RemoteServerDist("SNAPSHOT", RemoteServerDistTest.test_config_with_jenkins)
        self.temp_dir = self.create_temp_dir()

    @unittest.skipUnless(test_config_with_jenkins.has_section("jenkins"), "requires jenkins credentials")
    def test_download_server_dist_from_jenkins(self):
        downloaded_file = self.dist.download(self.temp_dir)
        self.assertIsNotNone(downloaded_file)
        self.assertTrue(path.isfile(downloaded_file))



