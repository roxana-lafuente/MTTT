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
from diff2html import Diff2HTML

class PostEditing:

    def __init__(self, post_editing_source_label, post_editing_reference_label, back_button, next_button, REC_button, notebook, postEditing_file_menu_grid, user_local_repository_path):
        self.post_editing_source = post_editing_source_label
        self.post_editing_reference = post_editing_reference_label
        self.back_button = back_button
        self.next_button = next_button
        self.REC_button = REC_button
        self.postEditing_file_menu_grid = postEditing_file_menu_grid
        self.user_local_repository_path = user_local_repository_path
        self.notebook = notebook
        self.alreadyAddedGitStatistics = False
        self.diff2html = Diff2HTML(self.user_local_repository_path)

    def calculateGitStatistics(self, filename):
        self.diff2html.calculateGitStatistics(filename)

    def addGitStatistics(self):
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

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        scrolledwindow.add(childWidget)
        self.notebook.append_page(scrolledwindow, Gtk.Label('Statistics'))
        self.notebook.show_all()

    def _saveChangedFromPostEditing(self):
        #reconstruct all cells from the table of the target column
        modified_reference = ""
        for index in range(0, len(self.translation_reference_text_lines)):
            if index in self.translation_reference_text_TextViews_modified_flag:
                modified_reference += self.translation_reference_text_TextViews_modified_flag[index]
            else:
                modified_reference += self.translation_reference_text_lines[index]
        #save to file
        i = self.post_editing_reference.get_text().rfind('/')
        filename = self.post_editing_reference.get_text()[i:]
        i = self.post_editing_reference.get_text().rfind('.')
        filename_without_extension = os.path.splitext(filename)[0]
        filename_extension = os.path.splitext(filename)[1]
        #lets see how using closure is seen by the team... here's hope it plays out!
        def savefile(text, filename):
            text_file = open(filename, "w")
            text = self.diff2html.prepare_text_for_HTML_output(text)
            text_file.write(text)
            text_file.close()
        savefile('\n'.join(self.translation_reference_text_lines), self.user_local_repository_path + filename)
        savefile(modified_reference, self.user_local_repository_path + filename_without_extension + "_modified" + filename_extension)

        if not self.alreadyAddedGitStatistics:
            self.alreadyAddedGitStatistics = True
            self.calculateGitStatistics(filename)
            self.addGitStatistics()

        self.changesMadeWorthSaving = 0
        self.postEditing_file_menu_grid.remove(self.save_post_editing_changes_button)

    def _saveChangedFromPostEditing_event(self, button):
        self._saveChangedFromPostEditing()

    def _search_button_action(self, button, line_index):
        self._move_in_translation_table(line_index - self.translation_table_index - 1)

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
            for line in self.translation_reference_text_lines:
                line_index += 1
                if text_to_search_for in line:
                    self.create_search_button(line, line_index)

    def search_and_mark(self, text_to_search_for, start, text_buffer):
        end = text_buffer.get_end_iter()
        match = start.forward_search(text_to_search_for, 0, end)

        if match != None:
            match_start, match_end = match
            tagtable = text_buffer.get_tag_table()
            tag = tagtable.lookup("found")
            if tag is None: text_buffer.create_tag("found",background="yellow"); tag = tagtable.lookup("found")
            text_buffer.apply_tag(tag, match_start, match_end)
            self.search_and_mark(text_to_search_for, match_end, text_buffer)

    def cell_in_translation_table_changed(self, text_buffer_object, user_data):
        self.changesMadeWorthSaving += 1
        if self.changesMadeWorthSaving == 1:
            #add save button
            self.save_post_editing_changes_button = Gtk.Button()
            self.save_post_editing_changes_button.set_image(Gtk.Image(stock=Gtk.STOCK_SAVE))
            self.save_post_editing_changes_button.set_label("Save changes")
            self.save_post_editing_changes_button.show()
            self.save_post_editing_changes_button.connect("clicked", self._saveChangedFromPostEditing_event)
            self.postEditing_file_menu_grid.attach(self.save_post_editing_changes_button, 3, 0, 1 ,1)
            if self.REC_button.get_active():
                self._saveChangedFromPostEditing()
        def fix_text(text):
            new_line_index = text.rfind("\n")
            if new_line_index == -1:
                text += "\n"
            return text
        text = fix_text(text_buffer_object.get_text(text_buffer_object.get_start_iter(),text_buffer_object.get_end_iter(),True) )
        self.translation_reference_text_TextViews_modified_flag[user_data] = text
        self.translation_reference_text_TextViews[user_data].override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 113, 44, 0.5))

    def _fill_translation_table(self):
        if self.post_editing_source.get_text() != "" and self.post_editing_reference.get_text() != "":
            with open(self.post_editing_source.get_text()) as fp:
                for line in fp:
                    line = unicode(line, 'iso8859-15')
                    if line != '\n':
                        self.translation_source_text_lines.append(line)

            with open(self.post_editing_reference.get_text()) as fp:
                for line in fp:
                    line = unicode(line, 'iso8859-15')
                    if line != '\n':
                        self.translation_reference_text_lines.append(line)


    def _translation_table_initializing(self):

        self.translation_source_text_TextViews = {}
        self.translation_reference_text_TextViews = {}
        self.translation_source_text_TextViews_modified_flag = {}
        self.translation_reference_text_TextViews_modified_flag = {}
        self.translation_source_text_lines = []
        self.translation_reference_text_lines = []
        self.search_buttons_array = []
        self.ammount_of_rows_in_translation_table = 5
        self.translation_table_index = 0

        self.translation_table = Gtk.Table(1,1, True)
        self.search_buttons_table = Gtk.Table(1,1, True)
        source_label = Gtk.Label("Source")
        self.translation_table.attach(source_label, 1, 1+1, 0, 1+0)
        target_label = Gtk.Label("Target")
        self.translation_table.attach(target_label, 2, 2+1, 0, 1+0)
        self.translation_table.set_col_spacings(5)
        self.translation_table.set_row_spacings(5)
        self.translation_table.set_homogeneous(False)

        return self.translation_table

    def _clean_translation_table(self):
        children = self.translation_table.get_children();
        for element in children:
            #remove all Gtk.Label and Gtk.TextView objects
            if isinstance(element,Gtk.TextView) or isinstance(element,Gtk.Label):
                self.translation_table.remove(element)
        #re-attach the source and target labels
        source_label = Gtk.Label("Source")
        source_label.show()
        self.translation_table.attach(source_label, 1, 1+1, 0, 1+0)
        target_label = Gtk.Label("Target")
        target_label.show()
        self.translation_table.attach(target_label, 2, 2+1, 0, 1+0)

    def _move_in_translation_table(self, ammount_of_lines_to_move, feel_free_to_change_the_buttons = True):
        #TODO move the following statement elsewhere
        if len(self.translation_source_text_lines) == 0:
            self._fill_translation_table()
        #clean the translation_table
        self._clean_translation_table()
        if ammount_of_lines_to_move > 0 or self.translation_table_index > 0:
             self.translation_table_index += ammount_of_lines_to_move
        if self.translation_table_index == 0:
            self.back_button.set_visible(False)
        self.changesMadeWorthSaving = 0
        for y in range (0,self.ammount_of_rows_in_translation_table):
            try:
                cell = Gtk.TextView()
                cell.set_wrap_mode(True)
                cell.set_editable(False)
                cell.set_cursor_visible(False)
                cellTextBuffer = cell.get_buffer()
                index = y + self.translation_table_index
                cellTextBuffer.set_text(self.translation_source_text_lines[index])
                self.translation_source_text_TextViews[index] = cell
                if index in self.translation_source_text_TextViews_modified_flag:
                    self.translation_source_text_TextViews[index].override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 113, 44, 0.5))
                cell.set_right_margin(20)
                cell.set_wrap_mode(2)#2 == Gtk.WRAP_WORD
                cell.show()
                self.translation_table.attach(cell, 1, 1+1, 1+y, 1+1+y)

                cell = Gtk.TextView()
                cell.set_wrap_mode(True)
                cellTextBuffer = cell.get_buffer()
                index = y + self.translation_table_index
                cellTextBuffer.set_text(self.translation_reference_text_lines[index])
                self.translation_reference_text_TextViews[index] = cell
                if index in self.translation_reference_text_TextViews_modified_flag:
                    self.translation_reference_text_TextViews[index].override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 113, 44, 0.5))
                cellTextBuffer.connect("changed", self.cell_in_translation_table_changed, index)
                cell.set_right_margin(20)
                cell.set_wrap_mode(2)#2 == Gtk.WRAP_WORD
                cell.show()
                self.translation_table.attach(cell, 2, 2+1, 1+y, 1+1+y)
            except IndexError:
                self.next_button.set_visible(False)
        if feel_free_to_change_the_buttons:
            if ammount_of_lines_to_move == -1:
                self.next_button.set_visible(True)
            else:
                self.back_button.set_visible(True)

    def _back_in_translation_table(self, button):
        self._move_in_translation_table(-1)
    def _next_in_translation_table(self, button):
        self._move_in_translation_table(+1)
    def _increase_translation_table_rows(self, button):
        self.ammount_of_rows_in_translation_table += 1
        self.update_translation_table(False)
    def _reduce_translation_table_rows(self, button):
        if self.ammount_of_rows_in_translation_table > 1:
            self.ammount_of_rows_in_translation_table -= 1
            self.update_translation_table(False)
    def update_translation_table(self, to_change_the_buttons_or_not = True):
        self._move_in_translation_table(+1, to_change_the_buttons_or_not)
        self._move_in_translation_table(-1, to_change_the_buttons_or_not)
    def _check_if_both_files_are_choosen_post_edition(self,object):
        if self.post_editing_source.get_text() != "" and self.post_editing_reference.get_text() != "":
            self.update_translation_table()
