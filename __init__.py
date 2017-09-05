from UM.Platform import Platform

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("SiemensNXIntegrationPlugin")


def getMetaData():
    return {}


def register(app):
    # Solid works only runs on Windows.
    plugin_data = {}
    if Platform.isWindows():
        from .Installer import Installer
        plugin_data["extension"] = Installer()
    return plugin_data
