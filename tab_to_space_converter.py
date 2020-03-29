import sublime
import sublime_plugin


class TabToSpaceConverterCommand(sublime_plugin.TextCommand):
    def run(self, edit, previous_tab_size = None, all_views = False):
        if not previous_tab_size:
            sublime.status_message("You've to define previous_tab_size for the keybinding!")
            return

        if all_views:
            self.run_all_views(previous_tab_size)
        else:
            self.process(self.view, previous_tab_size)

    def run_all_views(self, previous_tab_size):
        for view in sublime.active_window().views():
            self.process(view, previous_tab_size)

    def process(self, view, previous_tab_size):
        current_tab_size = view.settings().get("tab_size")

        # Apply original tab size of the file.
        view.settings().set("tab_size", previous_tab_size)

        # This trick will correctly convert inline (not leading) tabs.
        view.run_command("expand_tabs", {"set_translate_tabs": True})  # Converts leading and inline tabs.
        view.run_command("unexpand_tabs", {"set_translate_tabs": True})  # Reverts leading tabs.

        # Revert to initial tab size.
        view.settings().set("tab_size", current_tab_size)

        # Final conversion to spaces.
        view.run_command("expand_tabs", {"set_translate_tabs": True})
