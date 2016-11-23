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
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
gi.require_version('WebKit', '3.0')
from gi.repository import WebKit
import os
import sys
import urlparse
import time
from git_tools import *

class PostEditing:

    def __init__(self, post_editing_source_label, post_editing_reference_label, notebook, postEditing_file_menu_grid, saved_absolute_path, user_local_repository_path, user_local_repository):
        self.post_editing_source = post_editing_source_label
        self.post_editing_reference = post_editing_reference_label
        self.postEditing_file_menu_grid = postEditing_file_menu_grid
        self.saved_absolute_path = saved_absolute_path
        self.user_local_repository_path = user_local_repository_path
        self.user_local_repository = user_local_repository
        self.notebook = notebook
        self.modified_references =  []
        self.saved_modified_references = []
        self.tables = {}
        self.tables_contents = {}
        self._table_initializing("diff_table")
        self._table_initializing("translation_table")
        self.make_table_interface("translation_table")
        self.changesMadeWorthSaving = 0

        log_filepath = self.saved_absolute_path + '/paulaslog.json'
        #TODO remove the following line, it destroys the last saved logs
        if os.path.exists(log_filepath):
            os.remove(log_filepath)

    def make_table_interface(self, table = "translation_table"):
        self.back_button = Gtk.Button("Back")
        self.tables_contents[table][self.menu_grid].add(self.back_button)
        self.next_button = Gtk.Button("Next")
        self.tables_contents[table][self.menu_grid].attach_next_to(self.next_button, self.back_button, Gtk.PositionType.RIGHT, 1, 10)
        self.reduce_rows_translation_table = Gtk.Button("- rows")
        self.tables_contents[table][self.menu_grid].attach_next_to(self.reduce_rows_translation_table, self.back_button, Gtk.PositionType.BOTTOM, 1, 10)
        self.increase_rows_translation_table = Gtk.Button("+ rows")
        self.tables_contents[table][self.menu_grid].attach_next_to(self.increase_rows_translation_table, self.next_button, Gtk.PositionType.BOTTOM, 1, 10)
        self.REC_button = Gtk.CheckButton.new_with_label("REC")
        self.tables_contents[table][self.menu_grid].attach_next_to(self.REC_button, self.next_button, Gtk.PositionType.RIGHT, 1, 10)
        self.tables_contents[table][self.menu_grid].set_column_spacing(10)

        self.post_editing_source.connect("changed", self._check_if_both_files_are_choosen_post_edition)
        self.post_editing_reference.connect("changed", self._check_if_both_files_are_choosen_post_edition)
        self.increase_rows_translation_table.connect("clicked", self._increase_table_rows,table)
        self.reduce_rows_translation_table.connect("clicked", self._reduce_table_rows,table)
        self.back_button.connect("clicked", self._back_in_table,table)
        self.next_button.connect("clicked", self._next_in_table,table)

    def calculateGitStatistics(self):
        import subprocess
        command = "python ./gitinspector-master/gitinspector.py " + self.user_local_repository_path + " -F html -T"
        html_output = []
        proc = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE)
        while True:
          line = proc.stdout.readline()
          if line != '': html_output.append(line)
          else: break
        filepath_complete = self.user_local_repository_path + "/index.html"
        text_file = open(filepath_complete, "w")
        text_file.write('\n'.join(html_output))
        text_file.close()

    def addGitStatistics(self):
        self.notebook.remove_page(6)
        html = "<h1>This is HTML content</h1><p>I am displaying this in python</p"
        win = Gtk.Window()
        view = WebKit.WebView()
        view.open(html)
        uri = self.user_local_repository_path + '/index.html'
        uri = os.path.realpath(uri)
        uri = urlparse.ParseResult('file', '', uri, '', '', '')
        uri = urlparse.urlunparse(uri)
        view.load_uri(uri)
        win.add(view)
        childWidget = win.get_child()
        win.remove(childWidget)
        win.destroy()

        self.notebook.insert_page(childWidget, Gtk.Label('Git Statistics'), 6)
        self.notebook.show_all()

    def addNonGitStatistics(self):
        self.preparation = Gtk.VBox()
        self.notebook.remove_page(5)

        self.tables["diff_table"] = Gtk.Table(1,1, True)
        source_label = Gtk.Label("Source")
        self.tables["diff_table"].attach(source_label, 1, 1+1, 0, 1+0)
        target_label = Gtk.Label("Target")
        self.tables["diff_table"].attach(target_label, 2, 2+1, 0, 1+0)
        self.tables["diff_table"].set_col_spacings(5)
        self.tables["diff_table"].set_row_spacings(5)
        self.tables["diff_table"].set_homogeneous(False)

        self.update_table("diff_table")

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        scrolledwindow.add(self.tables["diff_table"])
        grid = Gtk.Grid()

        term_search_frame = Gtk.Frame(label="Term Search")
        self.make_table_interface("diff_table")
        term_search_frame.add(self.tables_contents["diff_table"][6])
        grid.add(term_search_frame)
        #grid.add(self.tables_contents[table][self.rows_ammount])
        grid.set_row_spacing(1)
        grid.set_column_spacing(20)

        grid.attach_next_to(scrolledwindow, term_search_frame, Gtk.PositionType.BOTTOM, 1, 1)

        self.preparation.pack_start(grid, expand =True, fill =True, padding =0)
        self.notebook.insert_page(self.preparation, Gtk.Label('Non Git Statistics'), 5)
        self.notebook.show_all()

    def get_saved_origin_and_reference_filepaths(self):
        i = self.post_editing_reference.get_text().rfind('/')
        filename = self.post_editing_reference.get_text()[i:]
        i = self.post_editing_reference.get_text().rfind('.')
        filename_without_extension = os.path.splitext(filename)[0]
        filename_extension = os.path.splitext(filename)[1]

        saved_origin_filepath = self.saved_absolute_path + filename
        saved_reference_filepath = self.saved_absolute_path + filename_without_extension + "_modified" + filename_extension

        return (saved_origin_filepath,saved_reference_filepath)

    def save_not_using_git(self):
        #lets see how using closure is seen by the team... here's hope it plays out!
        def savefile(text, filename):
            text_file = open(filename, "w")
            #text = self.diff2html.prepare_text_for_HTML_output(text)
            text_file.write(text)
            text_file.close()
        saved_origin_filepath, saved_reference_filepath = self.get_saved_origin_and_reference_filepaths()
        savefile('\n'.join(self.tables_contents["translation_table"][1]), saved_origin_filepath)
        savefile('\n'.join(self.modified_references),saved_reference_filepath)

    def save_using_git(self):
        s = self.post_editing_reference.get_text()
        i = s.rfind('/')
        filename = s[i:]
        filepath_complete = self.user_local_repository_path  + filename
        saveNCommit(self.user_local_repository, filepath_complete, '\n'.join(self.modified_references))

    def save_using_paulas_version_of_a_version_control_system(self):
        import json
        paulaslog = {}
        log_filepath = self.saved_absolute_path + '/paulaslog.json'

        if not os.path.exists(log_filepath):
            open(log_filepath, 'w').close()
        else:
            with open(log_filepath) as json_data:
                paulaslog= json.load(json_data)


        for index in range(0, len(self.tables_contents["translation_table"][1])):
            if index in self.translation_reference_text_TextViews_modified_flag:
                modified_reference = self.translation_reference_text_TextViews_modified_flag[index]
                if modified_reference not in self.saved_modified_references:
                    self.saved_modified_references.append(modified_reference)
                    if self.last_change_timestamp not in paulaslog:
                        paulaslog[self.last_change_timestamp] = {}
                    paulaslog[self.last_change_timestamp][index] = modified_reference
        '''
        print "Just saved the following to paula's log:"
        print str(paulaslog)
        print "--------------"
        '''
        with open(log_filepath, 'w') as outfile:
            json.dump(paulaslog, outfile)

    def _saveChangedFromPostEditing(self):
        self.last_change_timestamp = int(time.time() * 1000)
        #reconstruct all cells from the table of the target column
        for index in range(0, len(self.tables_contents["translation_table"][1])):
            if index in self.translation_reference_text_TextViews_modified_flag:
                self.modified_references.append(self.translation_reference_text_TextViews_modified_flag[index])
            else:
                self.modified_references.append(self.tables_contents["translation_table"][1][index])

        self.save_not_using_git()
        string = self.post_editing_reference.get_text()
        self.addNonGitStatistics()

        #self.save_using_git()
        #self.calculateGitStatistics()
        #self.addGitStatistics()

        self.save_using_paulas_version_of_a_version_control_system()

        self.tables_contents["translation_table"][6].remove(self.save_post_editing_changes_button)

    def _saveChangedFromPostEditing_event(self, button):
        self._saveChangedFromPostEditing()

    def _search_button_action(self, button, line_index, table = "translation_table"):
        self._move_in_table(line_index - self.tables_contents[table][self.table_index] - 1, table)

    def create_search_button (self, text, line_index):
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
        search_button.connect("clicked", self._search_button_action, line_index)
        button_y_coordinate = len(self.search_buttons_array) -1
        self.search_buttons_table.attach(search_button, 0, 0+1, button_y_coordinate, button_y_coordinate+1)

    def search_and_mark_wrapper(self, text_buffer_object):
        text_to_search_for =  text_buffer_object.get_text()
        line_index = 0
        for a in self.search_buttons_array:
            a.destroy()
        self.search_buttons_array[:]=[]
        if text_to_search_for != "":
            for line in self.tables_contents["translation_table"][1]:
                line_index += 1
                if text_to_search_for.upper() in line.upper():
                    self.create_search_button(line, line_index)

    def cell_in_translation_table_changed(self, text_buffer_object, user_data):
        self.changesMadeWorthSaving += 1
        if self.changesMadeWorthSaving == 1:
            #add save button
            self.save_post_editing_changes_button = Gtk.Button()
            self.save_post_editing_changes_button.set_image(Gtk.Image(stock=Gtk.STOCK_SAVE))
            self.save_post_editing_changes_button.set_label("Save changes")
            self.save_post_editing_changes_button.show()
            self.save_post_editing_changes_button.connect("clicked", self._saveChangedFromPostEditing_event)
            self.tables_contents["translation_table"][6].attach(self.save_post_editing_changes_button, 3, 0, 1 ,1)
            if self.REC_button.get_active():
                self._saveChangedFromPostEditing()
        def fix_text(text):
            #in case the user deleted the endline character at the end of the text segment
            new_line_index = text.rfind("\n")
            if new_line_index == -1:
                text += "\n"
            return text
        text = fix_text(text_buffer_object.get_text(text_buffer_object.get_start_iter(),text_buffer_object.get_end_iter(),True) )
        self.translation_reference_text_TextViews_modified_flag[user_data] = text
        self.tables_contents["translation_table"][4][user_data].override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 113, 44, 0.5))

    def _fill_table(self, table = "translation_table"):
        origin = ""
        reference = ""
        if table == "translation_table":
            origin = self.post_editing_source.get_text()
            reference = self.post_editing_reference.get_text()
        elif table == "diff_table":
            origin, reference = self.get_saved_origin_and_reference_filepaths()
        if self.post_editing_source.get_text() != "" and self.post_editing_reference.get_text() != "":
            with open(origin) as fp:
                for line in fp:
                    line = unicode(line, 'iso8859-15')
                    if line != '\n':
                       self.tables_contents[table][self.source_text_lines].append(line)

            with open(reference) as fp:
                for line in fp:
                    line = unicode(line, 'iso8859-15')
                    if line != '\n':
                        self.tables_contents[table][self.reference_text_lines].append(line)


    def _table_initializing(self, table = "translation_table"):
        (self.source_text_lines,
        self.reference_text_lines,
        self.table_index,
        self.source_text_views,
        self.reference_text_views,
        self.rows_ammount,
        self.menu_grid,
        self.initialized) = range(8)
        #source_text_lines, reference_text_lines, table_index, source_text_views, reference_text_views, rows_ammount, menu_grid, initialized
        self.tables_contents[table] = [[],[],0,{},{}, 0, None, False]
        self.tables_contents[table][self.rows_ammount] = 5

        if table == "translation_table":
            self.translation_reference_text_TextViews_modified_flag = {}
            self.search_buttons_array = []
            self.tables_contents[table][self.menu_grid] = self.postEditing_file_menu_grid
        elif table == "diff_table":
            self.tables_contents[table][self.menu_grid] = Gtk.Grid()

        translation_table = Gtk.Table(1,1, True)
        self.tables[table] = translation_table
        self.search_buttons_table = Gtk.Table(1,1, True)
        source_label = Gtk.Label("Source")
        self.tables[table].attach(source_label, 1, 1+1, 0, 1+0)
        target_label = Gtk.Label("Target")
        self.tables[table].attach(target_label, 2, 2+1, 0, 1+0)
        self.tables[table].set_col_spacings(5)
        self.tables[table].set_row_spacings(5)
        self.tables[table].set_homogeneous(False)

        return self.tables[table]

    def _clean_translation_table(self, table = "translation_table"):
        table = self.tables[table]
        children = table.get_children();
        for element in children:
            #remove all Gtk.Label and Gtk.TextView objects
            if isinstance(element,Gtk.TextView) or isinstance(element,Gtk.Label):
                table.remove(element)
        #re-attach the source and target labels
        source_label = Gtk.Label("Source")
        source_label.show()
        table.attach(source_label, 1, 1+1, 0, 1+0)
        target_label = Gtk.Label("Target")
        target_label.show()
        table.attach(target_label, 2, 2+1, 0, 1+0)

    def create_cell(self, table, text, column_index, row_index, editable):
        cell = Gtk.TextView()
        cell.set_wrap_mode(True)
        cell.set_editable(editable)
        cell.set_cursor_visible(False)
        cellTextBuffer = cell.get_buffer()
        index = row_index + self.tables_contents[table][self.table_index]
        cellTextBuffer.set_text(self.tables_contents[table][self.source_text_lines][index])
        self.tables_contents[table][self.reference_text_views][index] = cell
        if index in self.translation_reference_text_TextViews_modified_flag:
            self.tables_contents[table][self.reference_text_views][index].override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 113, 44, 0.5))
        cellTextBuffer.connect("changed", self.cell_in_translation_table_changed, index)
        cell.set_right_margin(20)
        cell.set_wrap_mode(2)#2 == Gtk.WRAP_WORD
        cell.show()
        self.tables[table].attach(cell, column_index, column_index+1, 1+row_index, 1+1+row_index)

    def _move_in_table(self, ammount_of_lines_to_move, table = "translation_table", feel_free_to_change_the_buttons = True):
        if not self.tables_contents[table][self.initialized]:
            self.tables_contents[table][self.initialized] = True
            self._fill_table(table)
        #clean the translation_table
        self._clean_translation_table(table)
        if ammount_of_lines_to_move > 0 or self.tables_contents[table][self.table_index] > 0:
             self.tables_contents[table][self.table_index] += ammount_of_lines_to_move
        if self.tables_contents[table][self.table_index] == 0:
            self.back_button.set_visible(False)
        self.changesMadeWorthSaving = 0
        for row_index in range (0,self.tables_contents[table][self.rows_ammount]):
            try:
                self.create_cell(table, self.source_text_views, 1, row_index, False)
                self.create_cell(table, self.reference_text_views, 2, row_index, True)
            except IndexError:
                self.next_button.set_visible(False)
        if feel_free_to_change_the_buttons:
            if ammount_of_lines_to_move == -1:
                self.next_button.set_visible(True)
            else:
                self.back_button.set_visible(True)

    def _back_in_table(self, button, table = "translation_table"):
        self._move_in_table(-1, table)
    def _next_in_table(self, button, table = "translation_table"):
        self._move_in_table(+1,table)
    def _increase_table_rows(self, button, table = "translation_table"):
        self.tables_contents[table][self.rows_ammount] += 1
        self.update_table(table)
    def _reduce_table_rows(self, button, table = "translation_table"):
        if self.tables_contents[table][self.rows_ammount] > 1:
            self.tables_contents[table][self.rows_ammount] -= 1
            self.update_table(table)
    def update_table(self, table = "translation_table", to_change_the_buttons_or_not = False):
        self._move_in_table(+1,table, to_change_the_buttons_or_not)
        self._move_in_table(-1,table, to_change_the_buttons_or_not)
    def _check_if_both_files_are_choosen_post_edition(self,object):
        if self.post_editing_source.get_text() != "" and self.post_editing_reference.get_text() != "":
            self.update_table("translation_table", True)
