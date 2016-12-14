# !/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
#
# PyKeylogger: TTT for Linux and Windows
# Copyright (C) 2016 Roxana Lafuente <roxana.lafuente@gmail.com>
#                    Miguel Lemos <miguelemosreverte@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

#os is one of the modules that I know comes with 2.7, no questions asked.
import os

SHOW_STATISTICS = True
try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    from gi.repository import Gdk
    if not os.name == 'nt':  # Windows
        try:
            gi.require_version('WebKit', '3.0')
            from gi.repository import WebKit
        except: SHOW_STATISTICS= False
except ImportError:
    print "Dependency unfulfilled, please install gi library"
    exit(1)

def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
	try:
	        import pip
    	except ImportError:
		print "no pip"
		os.system('python get_pip.py')
	finally:
		import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

#these other ones I a am not so sure of. Thus the install function.
install_and_import("requests")
install_and_import("subprocess")
install_and_import("json")
install_and_import("sys")
install_and_import("time")
install_and_import("shutil")
install_and_import("urlparse")
install_and_import("itertools")
install_and_import("webbrowser")

from commands import *
from files_processing import *
from evaluation import *
from post_editing import PostEditing
from constants import moses_dir_fn

UI_INFO = """
<ui>
  <menubar name='MenuBar'>
    <menu action='VisualsMenu'>
      <menu action='Visuals'>
        <menuitem action='metro'/>
        <menuitem action='paper'/>
        <separator />
        <menuitem action='lights_on_option'/>
      </menu>
    </menu>
  </menubar>
</ui>
"""

class MyWindow(Gtk.Window):

    def __init__(self):
        # Recognize OS
        if os.name == 'posix':  # Linux
            self.is_linux, self.is_windows = True, False
        elif os.name == 'nt':  # Windows
            self.is_linux, self.is_windows = False, True
        else:
            print "Unknown OS"
            exit(1)
        # Check Moses Config file.
        self.moses_dir = ""
        try:
            f = open(moses_dir_fn, 'r')
            self.moses_dir = f.read()
            f.close()
        except IOError, OSError:
            # File does not exist.
            self.moses_dir = self.get_moses_dir()
            f = open(moses_dir_fn, 'w')
            f.write(self.moses_dir)
            f.close()
        finally:
            # File content is wrong
            if not self.is_moses_dir_valid(self.moses_dir):
                moses_dir = self.get_moses_dir()
                f = open(moses_dir_fn, 'w')
                f.write(self.moses_dir)
                f.close()

        self.saved_absolute_path = os.path.abspath("saved")
        self.saved_relative_filepath = "./saved"
        if not os.path.exists(self.saved_absolute_path):
            os.makedirs(self.saved_absolute_path)

        # Main title
        Gtk.Window.__init__(self, title="Translators' Training Tool")
        self.connect('destroy', self.final_responsabilities)
        self.set_border_width(3)

        # Toolbar initialization
        action_group = Gtk.ActionGroup("my_actions")
        self.add_choices_menu_actions(action_group)
        uimanager = self.create_ui_manager()
        uimanager.insert_action_group(action_group)
        menubar = uimanager.get_widget("/MenuBar")
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(menubar, False, False, 0)
        self.gtk_theme = "paper"
        self.lightsOption = "gtk"

        # Set notebook for tabs
        self.notebook = Gtk.Notebook()
        box.pack_start(self.notebook, True, True, 0)
        self.add(box)

        # Add tabs to the notebook
        self.is_corpus_preparation_ready = False
        # Corpus Preparation tab
        self._set_corpus_preparation()
        # LM & MT Training tab
        self._set_training()
        # Translation tab
        self._set_translation()
        # Evaluation tab
        self._set_evaluation()
        # Post Editing tab
        self._set_post_editing()
        # Init
        self.source_lang = None
        self.target_lang = None
        self.cwd = os.getcwd()

    def _check_moses_installation(self, directory):
        # TODO: TRY catch OSError when permission denied!!
        file_content = [f for f in os.listdir(directory)]
        moses_files = ["/scripts/tokenizer/tokenizer.perl",
                       "/scripts/recaser/truecase.perl",
                       "/scripts/training/clean-corpus-n.perl",
                       "/bin/lmplz",
                       "/bin/build_binary",
                       "/scripts/training/train-model.perl",
                       "/bin/moses"
                      ]
        if self.is_windows:
            moses_files = [f.replace("/", "\\")
                           for f in moses_files]
            moses_files = [f + ".exe"
                           for f in moses_files
                           if "/bin" in f]
        is_valid = True
        for mfile in moses_files:
            is_valid = is_valid and os.path.isfile(directory + mfile)
        return is_valid

    def is_moses_dir_valid(self, directory):
        is_valid = True
        if directory == "":
            is_valid = False   # Empty string
        elif not os.path.exists(directory):
            is_valid = False  # Directory does not exist
        else:
            # Check if dir exists but does not contain moses installation
            is_valid = self._check_moses_installation(directory)

        return is_valid

    def get_moses_dir(self):
        """
            Gets Moses directory.
        """
        directory = self.moses_dir
        response = Gtk.ResponseType.ACCEPT
        while response == Gtk.ResponseType.ACCEPT and not self.is_moses_dir_valid(directory):
            label = Gtk.Label("Enter moses installation directory")
            entry = Gtk.Entry()
            button = Gtk.Button("Choose File")
            button.connect("clicked", self._on_dir_clicked, entry)
            dialog = Gtk.Dialog("My dialog",
                                None,
                                Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                                (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
                                 Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
            box = dialog.get_content_area()
            box.add(label)
            box.add(entry)
            box.add(button)
            label.show()
            entry.show()
            button.show()
            response = dialog.run()
            directory = entry.get_text()
            dialog.destroy()

        # If it is not valid, keep asking until valid or user leaves.
        if response in [Gtk.ResponseType.REJECT,
                        Gtk.ResponseType.DELETE_EVENT]:
            # TODO: Show error and exit
            exit(1)
        else: # Gtk.ResponseType.ACCEPT
            self.moses_dir = directory

        return directory

    def _on_languages_combo_changed(self, combo, attribute):
        if attribute == "ST":
            self.source_lang = combo.get_active_text()
        elif attribute == "TT":
            self.target_lang = combo.get_active_text()

    def _set_corpus_preparation(self):
        self.preparation = Gtk.VBox()
        grid = Gtk.Grid()
        inside_grid = Gtk.Grid()

        # Languages Frame.
        lang_frame = Gtk.Frame(label="Languages")
        # Source language picker
        stlang_label = Gtk.Label("Source text")
        inside_grid.add(stlang_label)
        self.stlang_box = Gtk.ComboBoxText()
        self.stlang_box.set_entry_text_column(0)
        self.stlang_box.connect("changed",
                                self._on_languages_combo_changed,
                                "ST")
        for language in languages:
            self.stlang_box.append_text(language)
        inside_grid.add(self.stlang_box)
        # Target language picker
        ttlang_label = Gtk.Label("Target text")
        inside_grid.attach_next_to(ttlang_label,
                                   stlang_label,
                                   Gtk.PositionType.BOTTOM,
                                   1,
                                   1)
        self.ttlang_box = Gtk.ComboBoxText()
        self.ttlang_box.set_entry_text_column(0)
        self.ttlang_box.connect("changed",
                                self._on_languages_combo_changed,
                                "TT")
        for language in languages:
            self.ttlang_box.append_text(language)
        inside_grid.attach_next_to(self.ttlang_box,
                                   self.stlang_box,
                                   Gtk.PositionType.BOTTOM,
                                   1,
                                   1)
        inside_grid.set_column_spacing(10)
        filler = Gtk.Label("   ")
        grid.attach(filler, 0, 0, 1, 1)
        lang_frame.add(inside_grid)
        grid.add(lang_frame)

        # Translation Model Frame.
        inside_grid = Gtk.Grid()
        tm_frame = Gtk.Frame(label="Translation Model")
        # Translation Model: Source Text Picker
        st_label = Gtk.Label("Source text")
        inside_grid.add(st_label)
        self.st_train = Gtk.Entry()
        self.st_train.set_text("")
        inside_grid.add(self.st_train)
        self.st_button = Gtk.Button("Choose File")
        self.st_button.connect("clicked", self._on_file_clicked, self.st_train)
        inside_grid.add(self.st_button)

        # Translation Model: Target Text Picker
        tt_label = Gtk.Label("Target text")
        inside_grid.attach_next_to(tt_label,
                                   st_label,
                                   Gtk.PositionType.BOTTOM,
                                   1,
                                   10)
        self.tt_train = Gtk.Entry()
        self.tt_train.set_text("")

        inside_grid.attach_next_to(self.tt_train,
                                   self.st_train,
                                   Gtk.PositionType.BOTTOM,
                                   1,
                                   1)
        self.tt_button = Gtk.Button("Choose File")
        self.tt_button.connect("clicked", self._on_file_clicked, self.tt_train)
        inside_grid.attach_next_to(self.tt_button,
                                   self.st_button,
                                   Gtk.PositionType.BOTTOM,
                                   1,
                                   1)
        inside_grid.set_column_spacing(10)
        tm_frame.add(inside_grid)
        grid.add(tm_frame)

        # Language Model Frame.
        lm_frame = Gtk.Frame(label="Language Model")
        # Align the label at the right of the frame.
        # lm_frame.set_label_align(1.0, 1.0)
        inside_grid = Gtk.Grid()
        inside_grid.add(Gtk.Label("Source text"))
        self.lm_text = Gtk.Entry()
        self.lm_text.set_text("")
        inside_grid.add(self.lm_text)
        self.lm_button = Gtk.Button("Choose File")
        self.lm_button.connect("clicked", self._on_file_clicked, self.lm_text)
        inside_grid.add(self.lm_button)
        lm_frame.add(inside_grid)
        grid.attach_next_to(lm_frame, tm_frame, Gtk.PositionType.BOTTOM, 1, 1)

        # Output directory.
        s_frame = Gtk.Frame(label="Settings")
        inside_grid = Gtk.Grid()
        inside_grid.add(Gtk.Label("Output directory"))
        self.output_text = Gtk.Entry()
        self.output_text.set_text("")
        inside_grid.add(self.output_text)
        self.s_button = Gtk.Button("Choose Directory")
        self.s_button.connect("clicked",
                              self._on_dir_clicked,
                              self.output_text)
        inside_grid.add(self.s_button)
        inside_grid.set_row_spacing(10)
        inside_grid.set_column_spacing(10)
        s_frame.add(inside_grid)
        grid.attach_next_to(s_frame, lm_frame, Gtk.PositionType.BOTTOM, 1, 1)

        # Start corpus preprocessing button.
        sbutton = Gtk.Button(label="Start corpus preprocessing")
        sbutton.connect("clicked", self._prepare_corpus)
        # self.preparation.set_border_width(10)
        grid.attach_next_to(sbutton, s_frame, Gtk.PositionType.BOTTOM, 1, 1)
        grid.set_row_spacing(20)
        grid.set_column_spacing(20)

        #self.preparation.add(grid)
        self.preparation.pack_start(grid,
                                    expand=True,
                                    fill=True,
                                    padding=30)
        self.notebook.insert_page(self.preparation,
                                  Gtk.Label('Corpus preparation'),0)

    def _prepare_corpus(self, button):
        win_output_directory = self.output_text.get_text()
        print "win_output_directory", win_output_directory
        output_directory = adapt_path_for_cygwin(self.is_windows, self.output_text.get_text())
        if output_directory is not None:
            # Change directory to the output_directory.
            try:
                os.chdir(win_output_directory)
            except:
                # Output directory does not exist.
                os.mkdir(win_output_directory)
                os.chdir(win_output_directory)
            cmds = []
            # 1) Tokenization
            # a) Target text
            self.target_tok = generate_input_tok_fn(self.target_lang,
                                                    output_directory)
            cmds.append(get_tokenize_command(adapt_path_for_cygwin(self.is_windows, self.moses_dir),
                                             self.target_lang,
                                             adapt_path_for_cygwin(self.is_windows,self.tt_train.get_text()),
                                             self.target_tok))
            # b) Source text
            self.source_tok = generate_input_tok_fn(self.source_lang,
                                                    output_directory)
            cmds.append(get_tokenize_command(adapt_path_for_cygwin(self.is_windows, self.moses_dir),
                                             self.source_lang,
                                             adapt_path_for_cygwin(self.is_windows,self.st_train.get_text()),
                                             self.source_tok))
            # c) Language model
            self.lm_tok = generate_lm_tok_fn(output_directory)
            cmds.append(get_tokenize_command(adapt_path_for_cygwin(self.is_windows, self.moses_dir),
                                             self.source_lang,
                                             adapt_path_for_cygwin(self.is_windows,self.tt_train.get_text()),
                                             self.lm_tok))

            # 2) Truecaser training
            # a) Target text
            cmds.append(get_truecaser_train_command(adapt_path_for_cygwin(self.is_windows, self.moses_dir),
                                                    self.target_tok))
            # b) Source text
            cmds.append(get_truecaser_train_command(adapt_path_for_cygwin(self.is_windows, self.moses_dir),
                                                    self.source_tok))
            # c) Language model
            cmds.append(get_truecaser_train_command(adapt_path_for_cygwin(self.is_windows, self.moses_dir),
                                                    self.lm_tok))

            # 3) Truecaser
            self.input_true = output_directory + "/input.true"
            # a) Target text
            self.target_true = generate_input_true_fn(self.target_lang,
                                                      output_directory)
            cmds.append(get_truecaser_command(adapt_path_for_cygwin(self.is_windows, self.moses_dir),
                                              self.target_tok,
                                              self.target_true))
            # b) Source text
            self.source_true = generate_input_true_fn(self.source_lang,
                                                      output_directory)
            cmds.append(get_truecaser_command(adapt_path_for_cygwin(self.is_windows, self.moses_dir),
                                              self.source_tok,
                                              self.source_true))
            # c) Language model
            self.lm_true = generate_lm_true_fn(output_directory)
            cmds.append(get_truecaser_command(adapt_path_for_cygwin(self.is_windows, self.moses_dir),
                                              self.target_tok, self.lm_true))

            # 4) Cleaner
            # a) Target text
            self.input_clean = generate_input_clean_fn(output_directory)
            self.source_clean = self.input_true + "." + self.source_lang
            self.target_clean = self.input_true + "." + self.target_lang
            cmds.append(get_cleaner_command(adapt_path_for_cygwin(self.is_windows, self.moses_dir),
                                             self.source_lang,
                                            self.target_lang,
                                            self.input_true,
                                            self.input_clean))

            # Start threads
            all_ok = True
            for cmd in cmds:
                print cmd
                # all_ok = all_ok and (os.system(cmd) == 0)
                proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
                all_ok = all_ok and (proc.wait() == 0)
                # print "returncode:", proc.returncode, "\n\n\n"
                out, err = proc.communicate()
            if all_ok:
                self.is_corpus_preparation_ready = True
        else:
            print "TODO: Pop up error message!!"

    def _on_file_clicked(self, widget, labelToUpdate):
        dialog = Gtk.FileChooserDialog("Please choose a file", None,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self._add_file_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            labelToUpdate.set_text(dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            labelToUpdate.set_text("")

        dialog.destroy()

    def _on_dir_clicked(self, widget, labelToUpdate):
        dialog = Gtk.FileChooserDialog("Please choose a directory", None,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self._add_dir_filters(dialog)
        dialog.set_action(Gtk.FileChooserAction.SELECT_FOLDER)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            labelToUpdate.set_text(dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            labelToUpdate.set_text("")

        dialog.destroy()

    def _add_dir_filters(self, dialog):
        # TODO: Allow to only choose folders
        filter_text = Gtk.FileFilter()

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def _add_file_filters(self, dialog):
        filter_text = Gtk.FileFilter()

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def _set_training(self):
        self.training = Gtk.Box()
        grid = Gtk.Grid()

        # Start training button.
        self.start_training_button = Gtk.Button("Start training")
        self.start_training_button.connect("clicked", self._train)
        grid.add(self.start_training_button)
        # Output label.
        training_results_frame = Gtk.Frame(label="Results")
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        resultsText = Gtk.TextView()
        resultsText.set_editable(False)
        resultsText.set_cursor_visible(False)
        resultsText.set_wrap_mode(True)
        self.trainingResultsTextBuffer = resultsText.get_buffer()
        scrolledwindow.add(resultsText)
        training_results_frame.add(scrolledwindow)
        grid.attach_next_to(training_results_frame,
                            self.start_training_button,
                            Gtk.PositionType.BOTTOM,
                            1,
                            1)

        self.training.add(grid)
        self.notebook.insert_page(self.training, Gtk.Label('Training'),1)

    def _train(self, button):
        # print "==============================>", self.is_corpus_preparation_ready
        output_directory = adapt_path_for_cygwin(self.is_windows, self.output_text.get_text())
        if output_directory is not None and self.is_corpus_preparation_ready:
            cmds = []
            output = "Log:\n\n"
            # Train the language model.
            self.lm_arpa = generate_lm_fn(output_directory)
            print "out:", self.lm_arpa, "\n"
            cmds.append(get_lmtrain_command(self.moses_dir,
                                             self.target_lang,
                                            self.lm_true,
                                            self.lm_arpa))

            # Binarize arpa
            self.blm = generate_blm_fn(output_directory)
            print "binarized out:", self.blm, "\n"
            cmds.append(get_blmtrain_command(self.moses_dir,
                                             self.target_lang,
                                             self.lm_arpa,
                                             self.blm))

            # Set output / error to the output label.
            # self.training_output_label.set_text(output)
            self.trainingResultsTextBuffer.set_text(output)

            # Train the translation model.
            out_file = generate_tm_fn(output_directory)
            cmds.append(get_tmtrain_command(self.moses_dir,
                                             self.source_lang,
                                            self.target_lang,
                                            self.blm,
                                            self.input_clean,
                                            output_directory))

            # TODO!
            # Binarize phase-table.gz
            # Binarize reordering-table.wbe-msd-bidirectional-fe.gz
            # Change PhraseDictionaryMemory to PhraseDictionaryCompact
            # Set the path of the PhraseDictionary feature to point to $HOME/working/binarised-model/phrase-table.minphr
            # Set the path of the LexicalReordering feature to point to $HOME/working/binarised-model/reordering-table

            for cmd in cmds:
                # use Popen for non-blocking
                print cmd
                output += cmd
                proc = subprocess.Popen([cmd],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True)
                proc.wait()
                (out, err) = proc.communicate()
                if out != "":
                    output += out
                elif err != "":
                    output += err

            # Adding output from training.out
            training = adapt_path_for_cygwin(self.is_windows, self.output_text.get_text()) + "/training.out"
            try:
                with open(training, "r") as f:
                   output += "\n" + f.read()
            except IOError:
                output += "Error. Unsuccessful when attempting to create moses.ini"

            # Set output to the output label.
            self.trainingResultsTextBuffer.set_text(output)
        else:
            output = "ERROR: Please go to the first tab and complete the process."
            self.trainingResultsTextBuffer.set_text(output)

    def _set_translation(self):
        self.translation = Gtk.Box()
        # Machine Translation Frame.
        grid = Gtk.Grid()
        inside_grid = Gtk.Grid()
        mt_frame = Gtk.Frame(label="Machine translation")
        # Source Text Picker
        mt_in_label = Gtk.Label("Source text file")
        inside_grid.add(mt_in_label)
        self.mt_in_text = Gtk.Entry()
        self.mt_in_text.set_text("")
        inside_grid.add(self.mt_in_text)
        self.mt_in_button = Gtk.Button("Choose File")
        self.mt_in_button.connect("clicked",
                                  self._on_file_clicked,
                                  self.mt_in_text)
        inside_grid.add(self.mt_in_button)

        # Target Text Picker
        mt_out_label = Gtk.Label("MT output file")
        inside_grid.attach_next_to(mt_out_label,
                                   mt_in_label,
                                   Gtk.PositionType.BOTTOM,
                                   1,
                                   10)
        self.mt_out_text = Gtk.Entry()
        self.mt_out_text.set_text("")
        inside_grid.attach_next_to(self.mt_out_text,
                                   self.mt_in_text,
                                   Gtk.PositionType.BOTTOM,
                                   1,
                                   10)
        self.mt_out_button = Gtk.Button("Choose File")
        self.mt_out_button.connect("clicked",
                                   self._on_file_clicked,
                                   self.mt_out_text)
        inside_grid.attach_next_to(self.mt_out_button,
                                   self.mt_in_button,
                                   Gtk.PositionType.BOTTOM,
                                   1,
                                   10)

         # Start machine translation button.
        sbutton = Gtk.Button(label="Start machine translation")
        sbutton.connect("clicked", self._machine_translation)
        inside_grid.attach_next_to(sbutton,
                                   self.mt_out_text,
                                   Gtk.PositionType.BOTTOM,
                                   1,
                                   10)

        mt_frame.add(inside_grid)
        grid.add(mt_frame)

        # Output label.
        # self.mt_output_label = Gtk.Label("")
        # grid.attach_next_to(self.mt_output_label,
        #                     mt_frame,
        #                     Gtk.PositionType.BOTTOM,
        #                     1,
        #                     10)
        # Output label.
        mt_training_results_frame = Gtk.Frame(label="Results")
        mtscrolledwindow = Gtk.ScrolledWindow()
        mtscrolledwindow.set_hexpand(True)
        mtscrolledwindow.set_vexpand(True)
        mtresultsText = Gtk.TextView()
        mtresultsText.set_editable(False)
        mtresultsText.set_cursor_visible(False)
        mtresultsText.set_wrap_mode(True)
        self.mttrainingResultsTextBuffer = mtresultsText.get_buffer()
        mtscrolledwindow.add(mtresultsText)
        mt_training_results_frame.add(mtscrolledwindow)
        grid.attach_next_to(mt_training_results_frame,
                            mt_frame,
                            Gtk.PositionType.BOTTOM,
                            1,
                            1)

        self.translation.add(grid)
        self.notebook.insert_page(self.translation,
                                  Gtk.Label('Machine Translation'),2)

    def _machine_translation(self, button):
        in_file = adapt_path_for_cygwin(self.is_windows, self.mt_in_text.get_text())
        out_file = adapt_path_for_cygwin(self.is_windows, self.mt_out_text.get_text())
        if in_file is not None and out_file is not None:
            output = "Running decoder....\n\n"
            # Run the decoder.
            cmd = get_test_command(self.moses_dir,
                                             adapt_path_for_cygwin(self.is_windows, self.output_text.get_text()) + "/train/model/moses.ini",
                                   in_file,
                                   out_file)
            # use Popen for non-blocking
            print cmd
            proc = subprocess.Popen([cmd],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=True)
            (out, err) = proc.communicate()
            f = open(out_file, 'r')
            mt_result = f.read()
            if mt_result == "":
                if out != "":
                    output += out
                elif err != "":
                    output += err
            else:
                output += "Best translation: " + mt_result

            f.close()
            # Set output to the output label.
            self.mttrainingResultsTextBuffer.set_text(output)
        else:
            print "TODO: Error pop-up message!!"

    def _set_evaluation(self):
        self.preparation = Gtk.VBox()
        grid = Gtk.Grid()

        # Evaluation Frame.
        inside_grid = Gtk.Grid()
        texts_menu_frame = Gtk.Frame(label="Evaluation")
        # Evaluation Metrics: Source Text Picker
        st_label = Gtk.Label("Source text")
        inside_grid.add(st_label)
        self.evaluation_source = Gtk.Entry()
        self.evaluation_source.set_text("")
        inside_grid.add(self.evaluation_source)
        self.st_button = Gtk.Button("Choose File")
        self.st_button.connect("clicked", self._on_file_clicked, self.evaluation_source)
        inside_grid.add(self.st_button)

        #  Evaluation Metrics: Reference Text Picker
        tt_label = Gtk.Label("Reference text")
        inside_grid.attach_next_to(tt_label, st_label, Gtk.PositionType.BOTTOM, 1, 10)
        self.evaluation_reference = Gtk.Entry()
        self.evaluation_reference.set_text("")
        inside_grid.attach_next_to(self.evaluation_reference, self.evaluation_source, Gtk.PositionType.BOTTOM, 1, 10)
        self.tt_button = Gtk.Button("Choose File")
        self.tt_button.connect("clicked", self._on_file_clicked, self.evaluation_reference)
        inside_grid.attach_next_to(self.tt_button, self.st_button, Gtk.PositionType.BOTTOM, 1, 10)
        inside_grid.set_column_spacing(10)

        #  Evaluation Metrics: Output Text Picker
        ot_label = Gtk.Label("Output directory")
        inside_grid.attach_next_to(ot_label, tt_label, Gtk.PositionType.BOTTOM, 1, 10)
        self.evaluation_output = Gtk.Entry()
        self.evaluation_output.set_text("")
        inside_grid.attach_next_to(self.evaluation_output, self.evaluation_reference, Gtk.PositionType.BOTTOM, 1, 10)
        self.ot_button = Gtk.Button("Choose File")
        self.ot_button.connect("clicked", self._on_file_clicked, self.evaluation_reference)
        inside_grid.attach_next_to(self.ot_button, self.tt_button, Gtk.PositionType.BOTTOM, 1, 10)
        inside_grid.set_column_spacing(10)

        texts_menu_frame.add(inside_grid)
        grid.add(texts_menu_frame)
        # Align the label at the right of the frame.
        # lm_frame.set_label_align(1.0, 1.0)
        grid.set_row_spacing(1)
        grid.set_column_spacing(20)


        # Evaluation Metrics Frame.
        inside_grid = Gtk.Grid()
        buttons_frame = Gtk.Frame(label="Evaluation Metrics")
        # Evaluation Metrics: Evaluations Picker
        self.check_WER = Gtk.CheckButton.new_with_label("WER")
        self.check_PER = Gtk.CheckButton.new_with_label("PER")
        self.check_HTER = Gtk.CheckButton.new_with_label("HTER")
        self.check_GTM = Gtk.CheckButton.new_with_label("GTM")
        self.check_BLEU = Gtk.CheckButton.new_with_label("BLEU")
        self.check_BLEU2GRAM = Gtk.CheckButton.new_with_label("BLEU2GRAM")
        self.check_BLEU3GRAM = Gtk.CheckButton.new_with_label("BLEU3GRAM")
        self.check_BLEU4GRAM = Gtk.CheckButton.new_with_label("BLEU4GRAM")
        inside_grid.add(self.check_WER)
        inside_grid.add(self.check_PER)
        inside_grid.add(self.check_HTER)
        inside_grid.add(self.check_GTM)
        inside_grid.attach_next_to(self.check_BLEU, self.check_WER, Gtk.PositionType.BOTTOM, 1, 1)
        inside_grid.attach_next_to(self.check_BLEU2GRAM, self.check_PER, Gtk.PositionType.BOTTOM, 1, 1)
        inside_grid.attach_next_to(self.check_BLEU3GRAM, self.check_HTER, Gtk.PositionType.BOTTOM, 1, 1)
        inside_grid.attach_next_to(self.check_BLEU4GRAM, self.check_GTM, Gtk.PositionType.BOTTOM, 1, 1)
        self.evaluate_button = Gtk.Button("Start evaluation ")
        self.evaluate_button.connect("clicked", self._evaluate)
        inside_grid.attach(self.evaluate_button, 0, 2, 3, 1)
        buttons_frame.add(inside_grid)
        grid.add(buttons_frame)

        # Evaluation: Results
        inside_grid = Gtk.Grid()
        evaluation_results_frame = Gtk.Frame(label="Results")
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        resultsText = Gtk.TextView()
        resultsText.set_editable(False)
        resultsText.set_cursor_visible(False)
        resultsText.set_wrap_mode(True)
        self.resultsTextBuffer = resultsText.get_buffer()
        scrolledwindow.add(resultsText)
        evaluation_results_frame.add(scrolledwindow)
        grid.attach(evaluation_results_frame, 0, 1, 3, 1)

        self.preparation.pack_start(grid, expand =True, fill =True, padding =0)
        self.notebook.insert_page(self.preparation, Gtk.Label('Evaluation'),3)

    def _evaluate(self, button):
        checkbox_indexes = [False] * 8 #checkbox_indexes["WER","PER","HTER", "GTM", "BLEU","BLEU2GRAM","BLEU3GRAM"]
        if self.check_WER.get_active():     checkbox_indexes[0] = True
        if self.check_PER.get_active():     checkbox_indexes[1] = True
        if self.check_HTER.get_active():    checkbox_indexes[2] = True
        if self.check_GTM.get_active():     checkbox_indexes[3] = True
        if self.check_BLEU.get_active():    checkbox_indexes[4] = True
        if self.check_BLEU2GRAM.get_active():   checkbox_indexes[5] = True
        if self.check_BLEU3GRAM.get_active():   checkbox_indexes[6] = True
        if self.check_BLEU4GRAM.get_active():   checkbox_indexes[7] = True
        result = evaluate(checkbox_indexes, self.evaluation_source.get_text(), self.evaluation_reference.get_text())
        self.resultsTextBuffer.set_text(result)

    def _set_post_editing(self):
        self.notebook.remove_page(4)
        self.preparation = Gtk.VBox()
        self.postEdition_grid = Gtk.Grid()
        self.postEdition_grid.set_row_spacing(1)
        self.postEdition_grid.set_column_spacing(20)

        #  Post Editing Frame.
        self.postEditing_file_menu_grid = Gtk.Grid()
        texts_menu_frame = Gtk.Frame(label="Post-Editing")
        # Post Editing : Source Text Picker
        post_editing_source_label = Gtk.Label("Select source file")
        self.postEditing_file_menu_grid.add(post_editing_source_label)
        self.post_editing_source = Gtk.Entry()
        self.post_editing_source.set_text("")
        self.postEditing_file_menu_grid.add(self.post_editing_source)
        self.post_editing_source_button = Gtk.Button("Choose File")
        self.post_editing_source_button.connect("clicked", self._on_file_clicked, self.post_editing_source)
        self.postEditing_file_menu_grid.add(self.post_editing_source_button)

        # Post Editing : Reference Text Picker
        post_editing_reference_label = Gtk.Label("Select MT file")
        self.postEditing_file_menu_grid.attach_next_to(post_editing_reference_label, post_editing_source_label, Gtk.PositionType.BOTTOM, 1, 10)
        self.post_editing_reference = Gtk.Entry()
        self.post_editing_reference.set_text("")
        self.postEditing_file_menu_grid.attach_next_to(self.post_editing_reference, self.post_editing_source, Gtk.PositionType.BOTTOM, 1, 10)
        self.post_editing_reference_button = Gtk.Button("Choose File")
        self.post_editing_reference_button.connect("clicked", self._on_file_clicked, self.post_editing_reference)
        self.postEditing_file_menu_grid.attach_next_to(self.post_editing_reference_button, self.post_editing_source_button, Gtk.PositionType.BOTTOM, 1, 10)
        self.post_editing_source.connect("changed", self._check_if_both_files_are_choosen_post_edition)
        self.post_editing_reference.connect("changed", self._check_if_both_files_are_choosen_post_edition)

        self.postEdition_grid.add(self.postEditing_file_menu_grid)
        self.preparation.pack_start(self.postEdition_grid, expand =True, fill =True, padding =0)
        self.notebook.insert_page(self.preparation, Gtk.Label('Post Editing'),4)
        self.notebook.show_all()

    def _check_if_both_files_are_choosen_post_edition(self,object):
        if self.post_editing_source.get_text() != "" and self.post_editing_reference.get_text() != "":
            post_editing_source_text = self.post_editing_source.get_text()
            post_editing_reference_text = self.post_editing_reference.get_text()
            self._set_post_editing()
            self.notebook.set_current_page(4)
            #binding of the buttons events to the PostEditing methods
            self.PostEditing = PostEditing(
                post_editing_source_text,#so that it can read the source file
                post_editing_reference_text,#so that it can read the reference file
                self.notebook,#so that it can add the diff tab when needed
                self.postEdition_grid)#so that it can add search entry and table

    def gtk_change_visuals(self, light_option = "unchanged", theme = "unchanged"):
        if Gtk.MAJOR_VERSION >=3 and  Gtk.MINOR_VERSION >=14:
            css_filename = "gtk"
            filename = ""
            if theme == "metro" or theme == "paper":
                self.gtk_theme = theme
            if light_option == "gtk" or light_option == "gtk-dark":
                self.lightsOption = light_option
            filename = 'gui/' + self.gtk_theme + '/'+ self.lightsOption + '.css'
            css = open(filename, 'r')

            style_provider = Gtk.CssProvider()
            css_data = css.read()
            css.close()

            style_provider.load_from_data(css_data)

            Gtk.StyleContext.add_provider_for_screen(
                Gdk.Screen.get_default(),
                style_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )

    def add_choices_menu_actions(self, action_group):
        self.preferences_button = Gtk.Action("VisualsMenu", "Preferences", None, None)
        action_group.add_action(self.preferences_button)
        action_visualsmenu = Gtk.Action("Visuals", "Visuals", None, None)
        action_group.add_action_with_accel(action_visualsmenu, None)
        action_group.add_radio_actions([
            ("metro", None, "metro", None, None, 1),
            ("paper", None, "paper", None, None, 2)
        ], 2, self.on_menu_choices_changed)

        lights_on_widget = Gtk.ToggleAction("lights_on_option", "Turn lights off", None, None)
        lights_on_widget.connect("toggled", self.on_menu_choices_toggled)
        action_group.add_action(lights_on_widget)

    def create_ui_manager(self):
        uimanager = Gtk.UIManager()
        uimanager.add_ui_from_string(UI_INFO)
        # Add the accelerator group to the toplevel window
        accelgroup = uimanager.get_accel_group()
        self.add_accel_group(accelgroup)
        return uimanager

    def on_menu_choices_changed(self, widget, current):
        self.gtk_change_visuals(light_option = "unchanged", theme = current.get_name())

    def on_menu_choices_toggled(self, widget):
        if widget.get_active():
            self.gtk_change_visuals(light_option = "gtk-dark",theme = "unchanged")
        else:
            self.gtk_change_visuals(light_option = "gtk",theme = "unchanged")
    def final_responsabilities(self, widget=None):
        if hasattr(self, 'PostEditing'):
            self.PostEditing.saveChangedFromPostEditing()
            self.PostEditing.delete_generated_files()

win = MyWindow()
win.gtk_change_visuals(light_option = "gtk", theme = "paper")
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
