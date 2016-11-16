import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from git_tools import GitWrapper

class Filling_User_Information():

    def retrieve_university_database(self):
        self.git = GitWrapper()
        self.git.clone_this("miguelemosreverte", "Alatriste007", "@github.com/GenevaOrFAMAF/UniversityDatabase.git")

    def parse_university_readme(self,line):

        if line != '\n' and line != '':
            if "#" in line:
                if "Siguientes Examenes" in line:
                    self.parsing_Examenes = False
                    self.parsing_Next_Examenes = True
                elif "Examenes" in line:
                    self.parsing_cursos = False
                    self.parsing_Examenes = True
            if "#" not in line:
                if self.parsing_cursos:
                    self.cursos.append(line)
                if self.parsing_Examenes:
                    self.examenes.append(line)
                if self.parsing_Next_Examenes:
                    self.next_examenes.append(line)

    def __init__(self):
        self.retrieve_university_database()
        self.DIR_NAME = self.git.get_dir_name()

        self.parsing_cursos = True
        self.parsing_Examenes = False
        self.parsing_Next_Examenes = False

        self.cursos = []
        self.examenes = []
        self.next_examenes = []

        self.famaf = False
        self.geneva = False

        Readme = self.DIR_NAME + "/README.md"
        with open(Readme) as fp:
            for line in fp:
                self.parse_university_readme(line)
        '''
        for curso in self.cursos:
            print curso
        print "-----------------"
        for examen in self.examenes:
            print examen
        print "-----------------"
        for next_examen in self.next_examenes:
            print next_examen
        print "-----------------"
        '''
        self.create_filling_window()

    def select_university(self):
        self.geneva_button.show()
        self.famaf_button.show()

    def select_curso(self):
        self.geneva_button.hide()
        self.famaf_button.hide()

        #cursos options
        self.cursos_buttons = []
        self.cursos_labels = []
        cursosL = Gtk.Label("Cursos:")
        self.VerticalBox.pack_start(cursosL, expand=True, fill = True, padding = 10)
        for curso in self.cursos:
            button = Gtk.CheckButton.new_with_label(curso)
            self.cursos_buttons.append(button)
            self.VerticalBox.pack_start(button, expand=True, fill = True, padding = 10)

        cursosL = Gtk.Label("Examenes del Dia:")
        self.cursos_labels.append(cursosL)
        self.VerticalBox.pack_start(cursosL, expand=True, fill = True, padding = 10)
        for examen in self.examenes:
            button = Gtk.CheckButton.new_with_label(examen)
            self.cursos_buttons.append(button)
            self.VerticalBox.pack_start(button, expand=True, fill = True, padding = 10)

        cursosL = Gtk.Label("Examenes Siguientes:")
        self.cursos_labels.append(cursosL)
        self.VerticalBox.pack_start(cursosL, expand=True, fill = True, padding = 10)
        for examen in self.next_examenes:
            button = Gtk.CheckButton.new_with_label(examen)
            self.cursos_buttons.append(button)
            self.VerticalBox.pack_start(button, expand=True, fill = True, padding = 10)

        self.done_button = Gtk.Button(label="Done")
        self.done_button.show()
        self.VerticalBox.pack_start(self.done_button, expand=True, fill = True, padding = 10)
        self.done_button.connect("clicked", self._done)
        self.VerticalBox.show()

        for label in self.cursos_labels:label.show()
        for button in self.cursos_buttons:button.show()

    def _done(self, button):
        self.filling_window.destroy()

    def _choose_university(self, button, university):
        if university == "famaf":
            self.famaf = True
        elif university == "geneva":
            self.geneva = True

        self.select_curso()

    def create_filling_window(self):
        self.filling_window = Gtk.Window()
        self.filling_window.set_title("Welcome")
        self.filling_window.connect("destroy", Gtk.main_quit)

        self.VerticalBox = Gtk.VBox(homogeneous=False, spacing=3)

        #universities options
        image = Gtk.Image()
        famaf_image = self.DIR_NAME + "/university_icons/famaf.jpg"
        image.set_from_file(famaf_image)
        image.show()
        self.famaf_button = Gtk.Button()
        self.famaf_button.add(image)
        self.famaf_button.hide()
        self.famaf_button.connect("clicked", self._choose_university, "famaf")
        self.VerticalBox.pack_start(self.famaf_button, expand=True, fill = True, padding = 10)
        image = Gtk.Image()
        geneva_image = self.DIR_NAME + "/university_icons/geneva.jpg"
        image.set_from_file(geneva_image)
        image.show()
        self.geneva_button = Gtk.Button()
        self.geneva_button.add(image)
        self.geneva_button.hide()
        self.geneva_button.connect("clicked", self._choose_university, "geneva")
        self.VerticalBox.pack_start(self.geneva_button, expand=True, fill = True, padding = 10)
        self.filling_window.add(self.VerticalBox)
        self.filling_window.show_all()
        self.select_university()


class Github_Login():


    def loginClicked(self,loginButton):
        self.repo_to_fork_name = "YourTypicalStudentRepo"
        self.repo_owner = "GenevaOrFAMAF"
        self.user = self.loginUserT.get_text()
        self.passwd = self.loginPassT.get_text()
        self.git = GitWrapper()
        logged_successfully = self.git.login_to_Github(self.user,self.passwd)
        if not logged_successfully: self.loginHbox3.set_visible(True)
        else:
            repoWasAlreadyForked = self.git.ifRepositoryIsNotForkedThenFork (self.repo_owner,self.repo_to_fork_name)
            self.login_window.destroy()

            if repoWasAlreadyForked: Gtk.main_quit()
            else: Filling_User_Information()
        #Filling_User_Information()

    def __init__(self):

        self.login_window = Gtk.Window()
        self.login_window.set_title("Login")
        #self.login_window.connect("destroy", Gtk.main_quit)
        loginVbox = Gtk.VBox(homogeneous=False)
        loginLabel = Gtk.Label("Login to Github")
        loginHbox1 = Gtk.HBox(homogeneous=False, spacing=3)
        loginHbox2 = Gtk.HBox(homogeneous=False, spacing=3)
        self.loginHbox3 = Gtk.HBox(homogeneous=False, spacing=3)
        loginUserL = Gtk.Label("Username:")
        loginPassL = Gtk.Label("Password:")
        loginFailed = Gtk.Label("Try Again")
        self.loginUserT = Gtk.Entry()
        self.loginPassT = Gtk.Entry()
        loginButton = Gtk.Button(label="Log In")
        loginButton.connect("clicked", self.loginClicked)

        self.login_window.add(loginVbox)
        loginVbox.pack_start(loginLabel, expand=False, fill = False, padding = 0)
        loginVbox.pack_start(loginHbox1, expand=False, fill = False, padding = 0)
        loginVbox.pack_start(loginHbox2, expand=False, fill = False, padding = 0)
        loginVbox.pack_start(self.loginHbox3, expand=False, fill = False, padding = 0)
        loginVbox.pack_start(loginButton, expand=True, fill = False, padding = 0)
        loginHbox1.pack_start(loginUserL, expand=False, fill = False, padding = 0)
        loginHbox1.pack_start(self.loginUserT, expand=True, fill = False, padding = 0)
        loginHbox2.pack_start(loginPassL, expand=False, fill = False, padding = 0)
        loginHbox2.pack_start(self.loginPassT, expand=True, fill = False, padding = 0)
        self.loginHbox3.pack_start(loginFailed, expand=True, fill = False, padding = 0)

        self.login_window.show_all()
        self.loginHbox3.set_visible(False)

        Gtk.main()
