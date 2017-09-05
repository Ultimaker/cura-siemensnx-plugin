import os
import subprocess

from UM.Extension import Extension
from UM.Logger import Logger
from UM.Message import Message
from UM.i18n import i18nCatalog
from UM.PluginRegistry import PluginRegistry

from cura.CuraApplication import CuraApplication

from PyQt5.QtCore import QObject

i18n_catalog = i18nCatalog("cura")


class Installer(QObject, Extension):
    def __init__(self, parent = None):
        super().__init__(parent)
        self._application = CuraApplication.getInstance()
        self.addMenuItem(i18n_catalog.i18n("Install"), self._install)

    def _install(self):
        files_path = os.path.abspath(os.path.join(PluginRegistry.getInstance().getPluginPath(self.getPluginId()), "files"))
        #self._set_key("UGII_USER_DIR", files_path)
        self._set_key_cmd("UGII_USER_DIR", files_path)

    def _set_key(self, name, value):
        from winreg import ConnectRegistry, OpenKey, SetValueEx, CloseKey, HKEY_CURRENT_USER, KEY_ALL_ACCESS, REG_EXPAND_SZ
        reg = None
        key = None
        try:
            path = r'Environment'
            reg = ConnectRegistry(None, HKEY_CURRENT_USER)
            key = OpenKey(reg, path, 0, KEY_ALL_ACCESS)
            SetValueEx(key, name, 0, REG_EXPAND_SZ, value)

        except Exception as e:
            print(e)

        if key:
            CloseKey(key)
        if reg:
            CloseKey(reg)

    def _set_key_cmd(self, name, value):
        args = ["setx", name, value]
        try:
            subprocess.run(args, check = True)
            message = Message("Successfully installed Siemens NX Cura plugin.")
            self._application.showMessage(message)
        except Exception as e:
            Logger.logException("e", "failed to set environment variable for Siemens NX")
