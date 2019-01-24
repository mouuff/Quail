from .installer_base import InstallerBase
import os
import pathlib

class InstallerOsx(InstallerBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    """ We need to put a syslink into /usr/local/bin or into a local folder inside the user's home directory"""
    def _register(self):
        self.__add_to_path(self.binary, self._binary_name)

    def _unregister(self):
        self.__remove_from_path(self.binary)

    def _registered(self):
        if not os.path.exists(self.build_symlink_path(self.binary)):
            return False

    def __add_to_path(self, binary, name):
        os.symlink(binary, self.build_symlink_path(name))

    def __remove_from_path(self, name):
        os.remove(self.build_install_path(name))

    def build_symlink_path(self, name):
        if self.install_systemwide:
            final_folder = '/usr/bin'
        else:
            final_folder = os.path.join(str(pathlib.Path.home()), '.local/bin')
        return os.path.join(final_folder, name)
