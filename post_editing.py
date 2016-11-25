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
import json
import os
import sys
import urlparse
import time
import itertools
from table import Table

class PostEditing:

    def __init__(self, post_editing_source, post_editing_reference, notebook, grid):
        self.post_editing_source = post_editing_source
        self.post_editing_reference = post_editing_reference
        self.translation_tab_grid = grid
        self.notebook = notebook
        self.modified_references =  []
        self.saved_modified_references = []

        self.tables = {}

        self.saved_absolute_path = os.path.abspath("saved")
        filename = post_editing_source[post_editing_source.rfind('/'):]
        filename_without_extension = os.path.splitext(filename)[0]
        filename_extension = os.path.splitext(filename)[1]
        self.saved_origin_filepath = os.path.abspath("saved") + filename
        self.saved_reference_filepath = os.path.abspath("saved") + filename_without_extension + "_modified" + filename_extension


        self.tables["translation_table"] =  Table("translation_table",self.post_editing_source,self.post_editing_reference, self._saveChangedFromPostEditing_event,self._saveChangedFromPostEditing,self.translation_tab_grid)

        self.paulas_log_filepath = self.saved_absolute_path + '/paulaslog.json'
        #TODO remove the following line, it destroys the last session saved logs
        #suggestion: load the last session saved logs, save it as old, and then do delete it.

        self.calculateStatistics()
        #if os.path.exists(self.paulas_log_filepath):
         #  os.remove(self.paulas_log_filepath)

    def calculateStatistics(self):
        paulaslog = self.load_paulas_log()
        self.seconds_spent_by_segment = {}
        #again with the closure, lets see how it plays out.
        def pairwise(iterable):
            a, b = itertools.tee(iterable)
            next(b, None)
            return itertools.izip(a, b)

        for current_timestamp,next_timestamp in pairwise(sorted(paulaslog.keys())):
            #for current_timestamp,next_timestamp in sorted(paulaslog.keys()):
            delta = (int(next_timestamp) - int(current_timestamp))/1000

            for segment_index in paulaslog[current_timestamp]:
                if segment_index in self.seconds_spent_by_segment:
                    self.seconds_spent_by_segment[segment_index] += delta
                else:
                    self.seconds_spent_by_segment[segment_index] = delta
        for a in self.seconds_spent_by_segment:
            print str(a) + "....." + str(self.seconds_spent_by_segment[a])

    def addStatistics(self):
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

    def load_paulas_log(self):
        paulaslog = {}
        if not os.path.exists(self.paulas_log_filepath):
            open(self.paulas_log_filepath, 'w').close()
        else:
            with open(self.paulas_log_filepath) as json_data:
                paulaslog= json.load(json_data)
        return paulaslog

    def save_using_paulas_version_of_a_version_control_system(self):
        paulaslog = {}
        paulaslog = self.load_paulas_log()


        for index in range(0, len(self.tables["translation_table"].tables_content[1])):
            if index in self.tables["translation_table"].translation_reference_text_TextViews_modified_flag:
                modified_reference = self.tables["translation_table"].translation_reference_text_TextViews_modified_flag[index]
                if modified_reference not in self.saved_modified_references:
                    self.saved_modified_references.append(modified_reference)
                    if self.last_change_timestamp not in paulaslog:
                        paulaslog[self.last_change_timestamp] = {}
                    paulaslog[self.last_change_timestamp][index] = modified_reference
        with open(self.paulas_log_filepath, 'w') as outfile:
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
        string = self.post_editing_reference

        self.diff_tab_grid = Gtk.Grid()
        self.diff_tab_grid.set_row_spacing(1)
        self.diff_tab_grid.set_column_spacing(20)
        self.tables["diff_table"] =  Table("diff_table",self.post_editing_source,self.post_editing_reference, self._saveChangedFromPostEditing_event,self._saveChangedFromPostEditing, self.diff_tab_grid)
        self.addDifferencesTab()

        self.save_using_paulas_version_of_a_version_control_system()

        self.tables["translation_table"].save_post_editing_changes_button.hide()


    def _saveChangedFromPostEditing_event(self, button):
        self._saveChangedFromPostEditing()
