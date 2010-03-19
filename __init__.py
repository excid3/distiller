"""
Distiller Rhythmbox Plugin

Version 1.0

Move selected songs to a specified directory

Author: Chris Oliver <excid3@gmail.com>

"""

import gtk
import os
import rb
import rhythmdb
import shutil
import urllib

destination = "~/Music"

icon_file = "/usr/share/icons/Humanity/places/24/folder-download.svg"
ui_str = """
<ui>
    <toolbar name="ToolBar">
        <placeholder name="ToolBarPluginPlaceholder">
            <toolitem name="Distill" action="Distill"/>
        </placeholder>
    </toolbar>
</ui>
"""

class Distiller(rb.Plugin):
    def activate(self, shell):
        ui = shell.get_ui_manager()

        # Load the icon
        iconsource = gtk.IconSource()
        iconsource.set_filename(icon_file)
        iconset = gtk.IconSet()
        iconset.add_source(iconsource)
        iconfactory = gtk.IconFactory()
        iconfactory.add("distiller-button", iconset)
        iconfactory.add_default()

        # Create actions for the plugin
        action = gtk.Action("Distill", "Distill",
                            "Move currently selected tracks",
                            "distiller-button")
        activate_id = action.connect("activate", self.distill, shell)

        # Group and its actions
        self.action_group = gtk.ActionGroup("DistillerActions")
        self.action_group.add_action(action)
        ui.insert_action_group(self.action_group, -1)

        # Add to the UI
        self.uid = ui.add_ui_from_string(ui_str)
        ui.ensure_update()        

    def deactivate(self, shell):
        # Clean up clean up everybody do your share
        ui = shell.get_ui_manager()
        ui.remove_ui(self.uid)
        ui.remove_action_group(self.action_group)

    def distill(self, event, shell):
        # Expand the destination path
        dest = os.path.expanduser(os.path.expandvars(destination))

        # Run through each of the selected songs
        for entry in shell.props.library_source.get_entry_view().get_selected_entries():

            # Get the file location in url format
            source = shell.props.db.entry_get(entry, rhythmdb.PROP_LOCATION)

            # Only handle file:/// ones for now
            if source.startswith("file:///"):

                # Create the destination folder if it doesn't exist
                if not os.path.exists(dest):
                    os.mkdir(dest)

                # Get a move on!
                shutil.move(urllib.url2pathname(source[7:]), dest)

