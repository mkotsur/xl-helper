import unittest
from xl_helper.artifacts.Plugin import Plugin


class PluginTest(unittest.TestCase):

    def test_plugin_or_not(self):
        assert Plugin.is_plugin("was-plugin-4.0.0.jar")
        assert Plugin.is_plugin("was-plugin-4.0.0-SNAPSHOT.jar")
        assert Plugin.is_plugin("jee-plugin-5.0.0-SNAPSHOT-xlPlugin.xldp")
        assert not Plugin.is_plugin("rocoto-6.2.jar")
        assert not Plugin.is_plugin("was-plugin-4.0.0.txt")
        assert not Plugin.is_plugin("readme.txt")

    def test_short_name(self):
        self.assertEqual(Plugin("was-plugin-4.0.0.jar").get_short_name(), "was")
        self.assertEqual(Plugin("was-plugin-4.0.0-SNAPSHOT.jar").get_short_name(), "was")
        self.assertEqual(Plugin("jee-plugin-5.0.0-xlPlugin.xldp").get_short_name(), "jee")
        self.assertEqual(Plugin("jee-plugin-5.0.0-SNAPSHOT-xlPlugin.xldp").get_short_name(), "jee")

    def test_version(self):
        self.assertEqual(Plugin("jee-plugin-5.0.0-SNAPSHOT-xlPlugin.xldp").get_version(), "5.0.0-SNAPSHOT")
        self.assertEqual(Plugin("jee-plugin-5.0.0-xlPlugin.xldp").get_version(), "5.0.0")
        self.assertEqual(Plugin("was-plugin-4.0.0.jar").get_version(), "4.0.0")
        self.assertEqual(Plugin("was-plugin-4.0.0-SNAPSHOT.jar").get_version(), "4.0.0-SNAPSHOT")

    def test_equality(self):
        self.assertTrue(Plugin('was-plugin-4.0.0') == Plugin('was-plugin-4.0.0'))
        self.assertTrue(Plugin('was-plugin-4.0.0-SNAPSHOT') == Plugin('was-plugin-4.0.0-SNAPSHOT'))
        self.assertTrue(Plugin('was-plugin-4.0.0') != Plugin('was-plugin-4.0.0-SNAPSHOT'))
        self.assertTrue(Plugin('was-plugin-4.1.0') != Plugin('was-plugin-4.0.0'))