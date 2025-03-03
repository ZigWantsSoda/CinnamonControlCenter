import gi
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk

class SettingsApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.example.SettingsApp",
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        self.window = Gtk.ApplicationWindow(application=self, title="Settings")
        self.window.set_default_size(900, 600)

        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.set_title("Settings")
        self.window.set_titlebar(header_bar)

        search_bar = Gtk.SearchEntry()
        search_bar.set_placeholder_text("Search settings...")
        search_bar.connect("search-changed", self.on_search_changed)
        header_bar.pack_end(search_bar)

        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.window.add(main_box)

        # Sidebar Scrolled Window
        sidebar_scrolled = Gtk.ScrolledWindow()
        sidebar_scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sidebar_scrolled.set_propagate_natural_height(True)
        sidebar_scrolled.set_size_request(250, -1)  # Fixed sidebar width
        main_box.pack_start(sidebar_scrolled, False, False, 0)

        # Sidebar Content Box
        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        sidebar.set_valign(Gtk.Align.START)
        sidebar.get_style_context().add_class("sidebar")

        # Add the sidebar to the scrolled window
        sidebar_scrolled.add(sidebar)

        # Main Content Area
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(300)
        main_box.pack_start(self.stack, True, True, 0)

        # Define sections and their respective options
        sections = {
            "Appearance": [
                ("Backgrounds", "preferences-desktop-wallpaper"),
                ("Effects", "preferences-desktop-effects"),
                ("Font Selection", "preferences-desktop-font"),
                ("Themes", "preferences-desktop-theme"),
            ],
            "Preferences": [
                ("Accessibility", "preferences-desktop-accessibility"),
                ("Account Details", "user-info"),
                ("Actions", "system-run"),
                ("Applets", "applications-applets"),
                ("Date & Time", "preferences-system-time"),
                ("Desklets", "applications-desklets"),
                ("Desktop", "preferences-desktop"),
                ("Extensions", "preferences-plugin"),
                ("General", "preferences-system"),
                ("Gestures", "input-touchpad"),
                ("Hot Corners", "preferences-desktop-screensaver"),
                ("Input Method", "preferences-desktop-keyboard"),
                ("Languages", "preferences-desktop-locale"),
                ("Night Light", "preferences-system-night-light"),
                ("Notifications", "preferences-desktop-notification"),
                ("Online Accounts", "preferences-system-network"),
                ("Panel", "preferences-desktop-panel"),
                ("Preferred Applications", "preferences-desktop-default-applications"),
                ("Privacy", "preferences-desktop-privacy"),
                ("Screensaver", "preferences-desktop-screensaver"),
                ("Startup Applications", "preferences-system-startup"),
                ("Windows", "preferences-system-windows"),
                ("Window Tiling", "preferences-desktop-window-tiling"),
                ("Workspaces", "preferences-desktop-workspaces"),
            ],
            "Hardware": [
                ("Bluetooth", "preferences-system-bluetooth"),
                ("Color", "preferences-desktop-color"),
                ("Disks", "preferences-system-disk-utility"),
                ("Display", "preferences-system-display"),
                ("Graphics Tablet", "input-tablet"),
                ("Keyboard", "input-keyboard"),
                ("Mouse and Touchpad", "input-mouse"),
                ("Network", "preferences-system-network"),
                ("Power Management", "preferences-system-power-management"),
                ("Printers", "preferences-system-printer"),
                ("Sound", "preferences-desktop-sound"),
                ("System Info", "system-information"),
            ],
            "Administration": [
                ("Driver Manager", "preferences-system-driver-manager"),
                ("Firewall", "preferences-system-firewall"),
                ("Login Window", "preferences-system-login"),
                ("Software Sources", "preferences-system-software-sources"),
                ("Users and Groups", "preferences-system-users"),
            ],
        }

        # Populate Sidebar and Stack
        for section, options in sections.items():
            # Section Title
            title_label = Gtk.Label(label=section)
            title_label.get_style_context().add_class("sidebar-title")
            title_label.set_halign(Gtk.Align.START)
            sidebar.pack_start(title_label, False, False, 0)

            for option, icon_name in options:
                button = Gtk.Button()
                button.get_style_context().add_class("sidebar-button")
                button.connect("clicked", self.on_category_selected, option)

                box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
                icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.BUTTON)
                label = Gtk.Label(label=option)

                box.pack_start(icon, False, False, 0)
                box.pack_start(label, False, False, 0)
                button.add(box)

                sidebar.pack_start(button, False, False, 0)

                # Add pages to stack
                page = self.create_page(option)
                self.stack.add_titled(page, option, option)

        self.load_css()
        self.window.show_all()

    def create_page(self, title):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        label = Gtk.Label(label=f"{title} Settings")
        label.get_style_context().add_class("settings-title")

        # Center the label
        label.set_halign(Gtk.Align.CENTER)
        label.set_valign(Gtk.Align.CENTER)

        page.pack_start(label, True, True, 0)
        return page

    def on_category_selected(self, button, page_name):
        self.stack.set_visible_child_name(page_name)
        for child in button.get_parent().get_children():
            child.get_style_context().remove_class("selected")
        button.get_style_context().add_class("selected")

    def on_search_changed(self, entry):
        query = entry.get_text().lower()
        for child in self.stack.get_children():
            if query in child.get_name().lower():
                self.stack.set_visible_child(child)

    def load_css(self):
        css_path = os.path.join(os.path.dirname(__file__), "style.css")
        if os.path.exists(css_path):
            css_provider = Gtk.CssProvider()
            css_provider.load_from_path(css_path)
            Gtk.StyleContext.add_provider_for_screen(
                Gdk.Screen.get_default(),
                css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
        else:
            print("Warning: style.css not found. Skipping CSS.")

app = SettingsApp()
app.run(None)

