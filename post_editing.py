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
import difflib
from table import Table

class PostEditing:

    def __init__(self, post_editing_source_label, post_editing_reference_label, notebook, grid, saved_absolute_path, user_local_repository_path, user_local_repository):
        self.post_editing_source = post_editing_source_label
        self.post_editing_reference = post_editing_reference_label
        self.translation_tab_grid = grid
        self.saved_absolute_path = saved_absolute_path
        self.user_local_repository_path = user_local_repository_path
        self.user_local_repository = user_local_repository
        self.notebook = notebook
        self.modified_references =  []
        self.saved_modified_references = []
        self.did_init_tags = False

        self.tables = {}

        i = self.post_editing_reference.get_text().rfind('/')
        filename = self.post_editing_reference.get_text()[i:]
        i = self.post_editing_reference.get_text().rfind('.')
        filename_without_extension = os.path.splitext(filename)[0]
        filename_extension = os.path.splitext(filename)[1]
        self.saved_origin_filepath = self.saved_absolute_path + filename
        self.saved_reference_filepath = self.saved_absolute_path + filename_without_extension + "_modified" + filename_extension


        self.tables["translation_table"] =  Table("translation_table",self.post_editing_source,self.post_editing_reference, self._saveChangedFromPostEditing_event,self._saveChangedFromPostEditing,self.saved_origin_filepath, self.saved_reference_filepath,self.translation_tab_grid)

        log_filepath = self.saved_absolute_path + '/paulaslog.json'
        #TODO remove the following line, it destroys the last saved logs
        if os.path.exists(log_filepath):
            os.remove(log_filepath)





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

    def addDifferencesTab(self):
        self.preparation = Gtk.VBox()
        self.notebook.remove_page(5)
        self.preparation.pack_start(self.diff_tab_grid, expand =True, fill =True, padding =0)
        self.notebook.insert_page(self.preparation, Gtk.Label('Differences'), 5)
        self.notebook.show_all()


    def save_not_using_git(self):
        #lets see how using closure is seen by the team... here's hope it plays out!
        def savefile(text, filename):
            text_file = open(filename, "w")
            text_file.write(text)
            text_file.close()
        savefile('\n'.join(self.tables["translation_table"].tables_content[self.tables["translation_table"].source_text_lines]), self.saved_origin_filepath)
        savefile('\n'.join(self.tables["translation_table"].tables_content[self.tables["translation_table"].reference_text_lines]),self.saved_reference_filepath)

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


        for index in range(0, len(self.tables["translation_table"].tables_contents["translation_table"][1])):
            if index in self.tables["translation_table"].translation_reference_text_TextViews_modified_flag:
                modified_reference = self.tables["translation_table"].translation_reference_text_TextViews_modified_flag[index]
                if modified_reference not in self.saved_modified_references:
                    self.saved_modified_references.append(modified_reference)
                    if self.last_change_timestamp not in paulaslog:
                        paulaslog[self.last_change_timestamp] = {}
                    paulaslog[self.last_change_timestamp][index] = modified_reference
        with open(log_filepath, 'w') as outfile:
            json.dump(paulaslog, outfile)

    def _saveChangedFromPostEditing(self):
        self.last_change_timestamp = int(time.time() * 1000)
        #reconstruct all cells from the table of the target column
        for index in range(0, len(self.tables["translation_table"].tables_content[1])):
            if index in self.tables["translation_table"].translation_reference_text_TextViews_modified_flag:
                self.modified_references.append(self.tables["translation_table"].translation_reference_text_TextViews_modified_flag[index])
            else:
                self.modified_references.append(self.tables["translation_table"].tables_content[1][index])

        self.save_not_using_git()
        string = self.post_editing_reference.get_text()

        self.diff_tab_grid = Gtk.Grid()
        self.diff_tab_grid.set_row_spacing(1)
        self.diff_tab_grid.set_column_spacing(20)
        self.tables["diff_table"] =  Table("diff_table",self.post_editing_source,self.post_editing_reference, self._saveChangedFromPostEditing_event,self._saveChangedFromPostEditing,self.saved_origin_filepath, self.saved_reference_filepath, self.diff_tab_grid)
        self.addDifferencesTab()

        #self.save_using_git()
        #self.calculateGitStatistics()
        #self.addGitStatistics()

        #self.save_using_paulas_version_of_a_version_control_system()

        self.tables["translation_table"].save_post_editing_changes_button.hide()


    def _saveChangedFromPostEditing_event(self, button):
        self._saveChangedFromPostEditing()
