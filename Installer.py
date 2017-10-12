import os
import subprocess
import shutil
import winreg

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

        # Automatically install the plugin
        CuraApplication.getInstance().callLater(self._install, True)

    ##  Installs the plugin. If this is called via auto-install, it won't show any message if everything goes fine.
    #   \param is_auto_install \type{bool} Whether this function is called via auto-install or not.
    def _install(self, is_auto_install = False):
        files_path = os.path.abspath(os.path.join(PluginRegistry.getInstance().getPluginPath(self.getPluginId()), "files"))

        existing_env_value = self._queryRegistryValue(winreg.HKEY_CURRENT_USER, "Environment", "UGII_USER_DIR")
        if existing_env_value is None:
            existing_env_value = os.environ.get("UGII_USER_DIR")
        if existing_env_value is not None:
            existing_env_value = os.path.abspath(existing_env_value)

        if existing_env_value is not None:
            if os.path.exists(existing_env_value):
                # if the path exists, check if it is a directory
                if not os.path.isdir(existing_env_value):
                    message = Message(i18n_catalog.i18n("Failed to copy Siemens NX plugins files. Please check your UGII_USER_DIR. It is not set to a directory."))
                    self._application.showMessage(message)
                    return

            # if it's the same directory, do nothing
            if existing_env_value == files_path:
                if not is_auto_install:
                    message = Message(i18n_catalog.i18n("Successfully installed Siemens NX Cura plugin."))
                    self._application.showMessage(message)
                return

            # If UGII_USER_DIR is already defined, try to copy the plugins file there.
            # The copying can fail because of permission or other reasons
            try:
                self._copyAllFiles(files_path, existing_env_value)
                if not is_auto_install:
                    message = Message(i18n_catalog.i18n("Successfully installed Siemens NX Cura plugin."))
                    self._application.showMessage(message)
            except Exception:
                Logger.logException("e", "Failed to copy files from [%s] to [%s]", files_path, existing_env_value)

                # show error message
                message = Message(i18n_catalog.i18n("Failed to copy Siemens NX plugins files. Please check your UGII_USER_DIR."))
                self._application.showMessage(message)
        else:
            # If the environment variable is not defined, set it as a user environment variable
            self._setUserEnvironmentVariable("UGII_USER_DIR", files_path)

    def _setUserEnvironmentVariable(self, name, value):
        """
        Sets the user environment variable for the Siemens NX plugins.
        :param name: Name of the environment variable.
        :param value: Value of the environment variable.
        """
        args = ["setx", name, value]
        try:
            os.environ[name] = value
            subprocess.run(args, check = True)
            message = Message(i18n_catalog.i18n("Successfully installed Siemens NX Cura plugin."))
            self._application.showMessage(message)
        except Exception:
            Logger.logException("e", "failed to set environment variable for Siemens NX")
            message = Message(i18n_catalog.i18n("Failed to install Siemens NX plugin. Could not set environment variable UGII_USER_DIR for Siemens NX."))
            self._application.showMessage(message)

    def _queryRegistryValue(self, main_key, path, name):
        reg = None
        key = None
        try:
            reg = winreg.ConnectRegistry(None, main_key)
            key = winreg.OpenKey(reg, path, 0, winreg.KEY_ALL_ACCESS)
            value, value_type = winreg.QueryValueEx(key, name)
            return value
        except Exception as e:
            Logger.log("i", "Could not find [%s] in the user environment variables: %s", name, e)
        finally:
            # close everything
            if key:
                try:
                    winreg.CloseKey(key)
                except:
                    pass
            if reg:
                try:
                    winreg.CloseKey(reg)
                except:
                    pass

    def _copyAllFiles(self, from_dir, to_dir):
        for name in os.listdir(from_dir):
            abs_from_path = os.path.join(from_dir, name)
            abs_to_path = os.path.join(to_dir, name)
            if os.path.isdir(abs_from_path):
                # make sure this directory is also in the target directory
                if not os.path.exists(abs_to_path):
                    # try to create the directory in the destination directory
                    try:
                        os.makedirs(abs_to_path)
                    except Exception as e:
                        raise RuntimeError("Could not create directory [%s]: %s", abs_to_path, e)
                elif os.path.exists(abs_to_path) and not os.path.isdir(abs_to_path):
                    raise RuntimeError("Could not copy files because the destination path [%s] is not a directory" % abs_to_path)

                # iterate into the directory
                self._copyAllFiles(abs_from_path, abs_to_path)

            elif os.path.isfile(abs_from_path):
                # copy the file there
                try:
                    shutil.copy2(abs_from_path, abs_to_path)
                except Exception as e:
                    raise RuntimeError("Could not copy file [%s] to [%s]: %s", abs_from_path, abs_to_path, e)
