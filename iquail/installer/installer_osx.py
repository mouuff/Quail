from .installer_base import InstallerBase
import os
import stat
import shutil
import pathlib
from ..helper import BundleTemplate, PlistCreator

class InstallerOsx(InstallerBase):

    def __init__(self, full_app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bundle_install_path = os.path.join(self._get_application_folder_path(), self.name + '.app')
        self.is_full_app = full_app

    """ TODO: Add the icon to the bundle"""
    def _register(self):
        if (self._should_register_as_pkg()):
            self._register_as_pkg()
            return
        if self.is_full_app:
            shutil.copytree(self.binary, os.path.join(self._get_application_folder_path(), self._binary_name))
            launcher_path = os.path.join(self._bundle_install_path, 'Contents', 'MacOS', self.name)
            st = os.stat(launcher_path)
            os.chmod(launcher_path, st.st_mode | stat.S_IEXEC)
            return
        else:
            bundle = BundleTemplate(self.name, base_dir=self._get_application_folder_path())
            icon_quail_path = self.get_solution_icon()
            bundle.make()
            if self._icon:
                bundle.installIcon(self._icon, icon_quail_path)
            plist = PlistCreator(self.name, self._get_application_folder_path(), {'CFBundleIconFile': self._icon})
            plist.build_tree_and_write_file()
            self._build_launcher()

    def _unregister(self):
        if (self._should_register_as_pkg()):
            #self._register_as_pkg()
            return
        shutil.rmtree(self._bundle_install_path)

    def _registered(self):
        if not os.path.exists(self.build_folder_path(self.binary)):
            return False
        return True

    def __add_to_path(self, binary, name):
        os.symlink(binary, self.build_folder_path(name))

    def _get_application_folder_path(self):
        if self.install_systemwide:
            return os.path.join(os.sep, 'Applications')
        return os.path.join(str(pathlib.Path.home()), 'Applications')

    def _should_register_as_pkg(self):
        if (self.binary.lower().endswith(".pkg")):
            return True
        return False

    def _register_as_pkg(self):
        path = os.path.join(self._solution_path, self.binary)
        pkg_installation = "installer -pkg " + path + " -target /"
        print(path)
        print(pkg_installation)
        os.system("/usr/bin/osascript -e 'do shell script \"" + pkg_installation + "\" with administrator privileges'")

    def build_folder_path(self, name):
        final_folder = os.path.join(self._get_application_folder_path(), self._name + '.app', 'Contents', 'MacOS')
        return os.path.join(final_folder, name)

    def _build_launcher(self):
        with open(os.path.join(self._bundle_install_path, 'Contents', 'MacOS', 'launcher'), 'w') as f:
            shebang = '#!/usr/bin/env bash\n'
            content = '/usr/bin/env python3 ' + self.launcher_binary
            f.write(shebang)
            f.write(content)
        st = os.stat(os.path.join(self._bundle_install_path, 'Contents', 'MacOS', 'launcher'))
        os.chmod(os.path.join(self._bundle_install_path, 'Contents', 'MacOS', 'launcher'), st.st_mode | stat.S_IEXEC)
