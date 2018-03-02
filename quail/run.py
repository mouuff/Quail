
import stat
import sys
import os
import argparse
import platform
from .Constants import Constants
from .Helper import *

if (platform.system() == 'Linux'):
    from .LinuxInstaller import LinuxInstaller
    Installer = LinuxInstaller
elif (platform.system() == 'Windows'):
    from .WindowsInstaller import WindowsInstaller
    Installer = WindowsInstaller
else:
    raise NotImplementedError


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(Constants.ARGUMENT_UNINSTALL,
                        help="uninstall program",
                        action="store_true")
    return parser.parse_args()


def run(config):
    '''run config'''
    args = parse_args()
    installer = Installer(**config)
    if args.quail_uninstall:
        installer.uninstall()
        sys.exit(0)
    if installer.is_installed():
        binary = installer.get_install_path(installer.get_binary())
        if not (stat.S_IXUSR & os.stat(binary)[stat.ST_MODE]):
            os.chmod(binary, 0o755)
        os.system(binary + " " + " ".join(sys.argv))
    else:
        installer.install()
