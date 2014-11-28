from distutils import dir_util
from os import path
import os
from xl_helper.FileUtils import FileUtils
from xl_helper.actions.Installer import Installer
from xl_helper.actions.Server import Server
import tempfile
import shutil
from xl_helper.artifacts.Plugin import Plugin
from xl_helper.artifacts.PluginsSelection import PluginsSelection


class Upgrader:

    def __init__(self, config):
        self.config = config

    def upgrade(self, home, to_dist, target=None):

        target = home if target is None else target
        server = Server.from_config(self.config, home)
        was_running = server.is_running()
        server.stop()

        print("Upgrading [%s] to version [%s] at [%s]" % (home, to_dist.version, target))

        temp_backup_dir = tempfile.mkdtemp("xld_backup")
        temp_install_dir = tempfile.mkdtemp("xld_backup")
        try:
            print("Creating backup at [%s]" % temp_backup_dir)
            FileUtils.move_contents(home, temp_backup_dir)

            print "Installing [%s]" % to_dist.version

            new_version_home = Installer(self.config).server(to_dist, temp_install_dir, None, was_running)
            FileUtils.move_contents(new_version_home, home)

            print "Copying files backup [%s] installation into [%s]" % (temp_backup_dir, home)
            if path.isdir(path.join(temp_backup_dir, 'repository')):
                dir_util.copy_tree(path.join(temp_backup_dir, 'repository'), path.join(home, 'repository'))

            dir_util.copy_tree(path.join(temp_backup_dir, 'plugins'), path.join(home, 'plugins'))
            dir_util.copy_tree(path.join(temp_backup_dir, 'conf'), path.join(home, 'conf'))
            dir_util.copy_tree(path.join(temp_backup_dir, 'ext'), path.join(home, 'ext'))
            self._remove_old_plugins(home)
        finally:
            shutil.rmtree(temp_backup_dir)
            shutil.rmtree(temp_install_dir)

        return target

    def _remove_old_plugins(self, server_location):
        plugins_path = path.join(server_location, 'plugins')
        for root, dirs, files in os.walk(plugins_path):
            plugins_selection = PluginsSelection(map(Plugin, filter(Plugin.is_plugin, files)))
            for op in plugins_selection.get_outdated_plugins():
                os.remove(path.join(plugins_path, op.filename))