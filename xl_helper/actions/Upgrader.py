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

        temp_backup_dir = None
        temp_install_dir = tempfile.mkdtemp("xld_install")

        target = home if target is None else FileUtils.ensure_empty_dir(target)

        if home == target:
            temp_backup_dir = tempfile.mkdtemp("xld_backup")
            print("Creating backup at [%s]" % temp_backup_dir)
            FileUtils.move_contents(home, temp_backup_dir)

        server = Server.from_config(self.config, home)
        was_running = server.is_running()
        server.stop()

        print("Upgrading [%s] to version [%s] at [%s]" % (home, to_dist.version, target))

        try:

            print "Installing [%s]" % to_dist.version

            new_version_home = Installer(self.config).server(to_dist, temp_install_dir, None, was_running)
            FileUtils.move_contents(new_version_home, home)

            print "Copying files backup [%s] installation into [%s]" % (temp_backup_dir, target)

            FileUtils.copy_subfolder(temp_backup_dir, target, 'repository')
            FileUtils.copy_subfolder(temp_backup_dir, target, 'plugins')
            FileUtils.copy_subfolder(temp_backup_dir, target, 'conf')
            FileUtils.copy_subfolder(temp_backup_dir, target, 'ext')
            self._remove_old_plugins(target)
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