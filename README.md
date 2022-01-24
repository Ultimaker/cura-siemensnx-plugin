# cura-siemensnx-plugin
Cura Plugin that integrates with Siemens NX.

This plug-in will install integration with Cura into your Siemens NX installation. No changes are made to Cura itself, but Siemens NX gets a new menu option to print the object with Cura. This option launches Cura or (if it's already open) loads the model into Cura.

Installation
----
To install this plug-in, open the Marketplace in Cura and find the Siemens NX plug-in there. If you have an Ultimaker account, you can also find it on [the online Marketplace](https://marketplace.ultimaker.com/app/cura/plugins/UltimakerPackages/SiemensNXIntegration) and add it to your account from there, to have Cura download it automatically for you.

Upon the next start-up of Cura, Cura will install the integration into your Siemens NX installation. You will then need to restart Siemens NX to be able to use the integration.

Usage
----
To use this integration, first create or open a design in Siemens NX. In the header bar, a new button will have appeared saying "Cura interface". Pressing this button opens a small dialogue, which allows you to select which body to export to Cura. When confirming, Cura will open with the new model loaded. You can slice it there and start printing.

If Cura was already open, it will replace the contents of the build plate in Cura with the new model. This way you can keep making design iterations in Siemens NX. When you want to update the model, simply export it from Siemens NX again. Cura will retain your ordinary settings, but per-object settings will be replaced with the model.
