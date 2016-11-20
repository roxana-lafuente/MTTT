import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from git import Repo
import os, shutil
from post_editing import PostEditing

class UserLogin():

    def retrieve_university_database(self):
        if os.path.exists(self.DIR_NAME):
            shutil.rmtree(self.DIR_NAME)
        os.makedirs(self.DIR_NAME)
        Repo.clone_from("https://github.com/GenevaOrFAMAF/UniversityDatabase", self.DIR_NAME)

    def __init__(self):
        #TODO DO NOT ALLOW USER TO ACCESS THIS FOLDER (./university database)
        self.DIR_NAME = "./university database"
        self.filepath = os.path.abspath("saved")
        self.user = "guest"
        self.retrieve_university_database()

        self.users = []
        usernames = self.DIR_NAME + "/users"
        with open(usernames) as fp:
            for line in fp:
                 self.users.append(line)

        self.create_login_window()
        Gtk.main()

    def search(self, text_buffer_object):
        text_to_search_for =  text_buffer_object.get_text()
        for a in self.search_buttons_array:
            a.destroy()
        self.search_buttons_array[:]=[]
        if text_to_search_for != "":
            for line in self.users:
                if text_to_search_for in line:
                    self.create_search_button(line)
        else:
            for line in self.users:
                self.create_search_button(line)

    def create_search_button (self, text):
        search_button = Gtk.Button()
        self.search_buttons_array.append(search_button)
        cell = Gtk.TextView()
        cell.set_wrap_mode(True)
        cellTextBuffer = cell.get_buffer()
        cellTextBuffer.set_text(text)
        cell.set_right_margin(20)
        cell.set_wrap_mode(2)#2 == Gtk.WRAP_WORD
        cell.show()
        search_button.add(cell)
        search_button.show()
        search_button.connect("clicked", self.loginClicked)
        button_y_coordinate = len(self.search_buttons_array) -1
        self.search_buttons_table.attach(search_button, 0, 0+1, button_y_coordinate, button_y_coordinate+1)

    def create_login_window(self):
        self.login_window = Gtk.Window()
        self.login_window.set_title("Welcome")
        self.login_window.connect("destroy", Gtk.main_quit)

        self.HorizontalBox = Gtk.HBox(homogeneous=False, spacing=3)

        image = Gtk.Image()
        famaf_image = "./resources/famaf.jpg"
        image.set_from_file(famaf_image)
        image.show()
        famaf_button = Gtk.Button()
        famaf_button.set_sensitive(False)
        famaf_button.add(image)
        self.HorizontalBox.pack_start(famaf_button, expand=True, fill = True, padding = 10)
        image = Gtk.Image()

        loginVbox = Gtk.VBox(homogeneous=False)
        loginHbox1 = Gtk.HBox(homogeneous=False, spacing=1)
        loginUserL = Gtk.Label("Username:")
        self.loginUserT = Gtk.Entry()
        self.loginUserT.connect("changed", self.search)


        loginVbox.pack_start(loginHbox1, expand=False, fill = True, padding = 0)
        loginHbox1.pack_start(loginUserL, expand=False, fill = True, padding = 0)
        loginHbox1.pack_start(self.loginUserT, expand=True, fill = True, padding = 0)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.search_buttons_table = Gtk.Table(1,1, True)
        self.search_buttons_array = []
        for line in self.users:
            self.create_search_button(line)
        scrolledwindow.add(self.search_buttons_table)

        loginVbox.pack_start(scrolledwindow, expand=True, fill = True, padding = 0)

        self.HorizontalBox.pack_start(loginVbox, expand=True, fill = True, padding = 0)


        self.login_window.show_all()

        geneva_image = "./resources/geneva.jpg"
        image.set_from_file(geneva_image)
        image.show()
        geneva_button = Gtk.Button()
        geneva_button.set_sensitive(False)
        geneva_button.add(image)
        self.HorizontalBox.pack_start(geneva_button, expand=True, fill = True, padding = 10)
        self.login_window.add(self.HorizontalBox)
        self.login_window.show_all()

    def get_user_local_repository_path(self):
        return self.filepath + "/" + self.user

    def get_user_local_repository(self):
        return self.user_local_repository

    def loginClicked(self,loginButton):
        textView = loginButton.get_child()
        text_buffer_object = textView.get_buffer()
        self.user = text_buffer_object.get_text(text_buffer_object.get_start_iter(),text_buffer_object.get_end_iter(),True)
        self.user = "".join(x for x in self.user if x.isalnum())
        self.user = self.user.strip()
        self.filepath = os.path.abspath("saved")
        self.relative_filepath = "./saved/" + self.user
        if not os.path.exists(self.relative_filepath):
            os.makedirs(self.relative_filepath)

        #self.user_local_repository = Repo.init(os.path.join(self.relative_filepath, self.user))
        self.login_window.destroy()
