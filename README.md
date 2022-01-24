# cura-siemensnx-plugin
Cura Plugin that integrates with Siemens NX.

This plug-in will install integration with Cura into your Siemens NX installation. No changes are made to Cura itself, but Siemens NX gets a new menu option to print the object with Cura. This option launches Cura or (if it's already open) loads the model into Cura.

Usage
----
To use this integration, first create or open a design in Siemens NX. In the header bar, a new button will have appeared saying "Cura interface". Pressing this button opens a small dialogue, which allows you to select which body to export to Cura. When confirming, Cura will open with the new model loaded. You can slice it there and start printing.

If Cura was already open, it will replace the contents of the build plate in Cura with the new model. This way you can keep making design iterations in Siemens NX. When you want to update the model, simply export it from Siemens NX again. Cura will retain your ordinary settings, but per-object settings will be replaced with the model.
