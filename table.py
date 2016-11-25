
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
import os
import sys
import difflib

class Table:
    def __init__(self, table_type, source, reference, save_callback_function,save_function, tab_grid):
        self.save_callback_function = save_callback_function
        self.save_function = save_function
        self.table_type = table_type
        self.source = source
        self.reference = reference
        self.tab_grid = tab_grid

        self.saved_origin_filepath = ""
        self.saved_reference_filepath = ""
        self.last_segment_changed = -1
        self._table_initializing()
        self.make_table_interface()
        self.update_table()

        self.modified_references =  []

        # Post Editing: Table
        search_frame = Gtk.Frame()
        search_results_scroll_window = Gtk.ScrolledWindow()
        search_results_scroll_window.set_hexpand(True)
        search_results_scroll_window.set_vexpand(True)
        search_results_scroll_window.add(self.table)
        search_frame.add(search_results_scroll_window)
        self.tab_grid.attach(search_frame, 0, 1, 2, 1)

        # Post Editing: Term Search
        table_frame = Gtk.Frame()
        table_scroll_window = Gtk.ScrolledWindow()
        table_scroll_window.show()
        term_search_frame = Gtk.Frame(label="Term Search")
        term_search_entry = Gtk.Entry()
        term_search_frame.add(term_search_entry)
        self.tab_grid.add(term_search_frame)
        term_search_entry.connect("changed", self.search_and_mark_wrapper)
        table_scroll_window.add(self.search_buttons_table)
        table_frame.add(table_scroll_window)
        self.tab_grid.attach_next_to(table_frame, term_search_frame, Gtk.PositionType.BOTTOM, 2, 1)

    def make_table_interface(self):
          self.back_button = Gtk.Button("Back")
          self.tables_content[self.get_menu_grid].add(self.back_button)
          self.next_button = Gtk.Button("Next")
          self.tables_content[self.get_menu_grid].attach_next_to(self.next_button, self.back_button, Gtk.PositionType.RIGHT, 1, 1)
          self.reduce_rows_translation_table = Gtk.Button("- rows")
          self.tables_content[self.get_menu_grid].attach_next_to(self.reduce_rows_translation_table, self.back_button, Gtk.PositionType.TOP, 1, 10)
          self.increase_rows_translation_table = Gtk.Button("+ rows")
          self.tables_content[self.get_menu_grid].attach_next_to(self.increase_rows_translation_table, self.next_button, Gtk.PositionType.TOP, 1, 10)
          self.tables_content[self.get_menu_grid].set_column_spacing(10)

          self.increase_rows_translation_table.connect("clicked", self._increase_table_rows)
          self.reduce_rows_translation_table.connect("clicked", self._reduce_table_rows)
          self.back_button.connect("clicked", self._back_in_table)
          self.next_button.connect("clicked", self._next_in_table)

          if self.table_type == "translation_table":
            #Add save buttons
            self.REC_button = Gtk.CheckButton.new_with_label("Autosave")
            self.tables_content[self.get_menu_grid].attach_next_to(self.REC_button, self.next_button, Gtk.PositionType.RIGHT, 1, 10)

            self.save_post_editing_changes_button = Gtk.Button()
            self.save_post_editing_changes_button.set_image(Gtk.Image(stock=Gtk.STOCK_SAVE))
            self.save_post_editing_changes_button.set_label("Save changes")
            self.save_post_editing_changes_button.connect("clicked", self.save_callback_function)
            self.tables_content[self.get_menu_grid].attach(self.save_post_editing_changes_button, 3, 0, 1 ,1)
            self.save_post_editing_changes_button.hide()


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
            for line in self.tables_content[1]:
                line_index += 1
                if text_to_search_for.upper() in line.upper():
                    self.create_search_button(line, line_index)

    def apply_tag(self, start,end, text_buffer, color = "yellow"):
        match_start = text_buffer.get_iter_at_offset(start)
        match_end = text_buffer.get_iter_at_offset(end)

        tagtable = text_buffer.get_tag_table()
        tag = tagtable.lookup(color)
        if color == "red": color = "#F8CBCB"
        if color == "green": color = "#A6F3A6"
        if tag is None: text_buffer.create_tag(color,background=color); tag = tagtable.lookup(color)
        text_buffer.apply_tag(tag, match_start, match_end)

    def cell_in_translation_table_changed(self, text_buffer_object, segment_index):
        self.save_post_editing_changes_button.show()
        if self.REC_button.get_active() and segment_index != self.last_segment_changed:
            self.save_function()
            self.last_segment_changed = segment_index

        def fix_text(text):
            #in case the user deleted the endline character at the end of the text segment
            new_line_index = text.rfind("\n")
            if new_line_index == -1:
                text += "\n"
            return text
        text = fix_text(text_buffer_object.get_text(text_buffer_object.get_start_iter(),text_buffer_object.get_end_iter(),True) )
        self.tables_content[self.reference_text_lines][segment_index] = text
        '''
        try:
            self.tables_contents["diff_table"][self.reference_text_lines][segment_index] = text
        except:pass
        '''

        self.translation_reference_text_TextViews_modified_flag[segment_index] = text
        self.tables_content[self.reference_text_views][segment_index].override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 113, 44, 0.5))

    def _fill_table(self):
        origin = self.source
        reference = self.reference

        saved_absolute_path = os.path.abspath("saved")
        filename = origin[origin.rfind('/'):]
        filename_without_extension = os.path.splitext(filename)[0]
        filename_extension = os.path.splitext(filename)[1]

        self.saved_origin_filepath = os.path.abspath("saved") + filename
        self.saved_reference_filepath = os.path.abspath("saved") + filename_without_extension + "_modified" + filename_extension

        if self.table_type == "diff_table":
            #then read the saved files
            origin = self.saved_origin_filepath
            reference = self.saved_reference_filepath

        if self.source != "" and self.reference != "":
            with open(origin) as fp:
                for line in fp:
                    line = unicode(line, 'iso8859-15')
                    if line != '\n':
                       self.tables_content[self.source_text_lines].append(line)

            with open(reference) as fp:
                for line in fp:
                    line = unicode(line, 'iso8859-15')
                    if line != '\n':
                        self.tables_content[self.reference_text_lines].append(line)


    def _table_initializing(self):
        (self.source_text_lines,
        self.reference_text_lines,
        self.table_index,
        self.source_text_views,
        self.reference_text_views,
        self.rows_ammount,
        self.get_menu_grid,
        self.initialized) = range(8)
        #source_text_lines, reference_text_lines, table_index, source_text_views, reference_text_views, rows_ammount, get_menu_grid, initialized
        self.tables_content = [[],[],0,{},{}, 0, None, False]
        self.tables_content[self.rows_ammount] = 5
        self.search_buttons_array = []

        if self.table_type == "translation_table":
            self.translation_reference_text_TextViews_modified_flag = {}
            self.tables_content[self.get_menu_grid] = Gtk.Grid()
            self.tab_grid.add(self.tables_content[self.get_menu_grid])
        elif self.table_type == "diff_table":
            self.tables_content[self.get_menu_grid] = Gtk.Grid()
            self.tab_grid.add(self.tables_content[self.get_menu_grid])
        table = Gtk.Table(1,1, True)
        self.table = table
        self.search_buttons_table = Gtk.Table(1,1, True)
        source_label = Gtk.Label("Source")
        self.table.attach(source_label, 1, 1+1, 0, 1+0)
        target_label = Gtk.Label("Target")
        self.table.attach(target_label, 2, 2+1, 0, 1+0)
        self.table.set_col_spacings(5)
        self.table.set_row_spacings(5)
        self.table.set_homogeneous(False)

        return self.table

    def _clean_table(self):
        children = self.table.get_children();
        for element in children:
            #remove all Gtk.Label and Gtk.TextView objects
            if isinstance(element,Gtk.TextView) or isinstance(element,Gtk.Label):
                self.table.remove(element)
        #re-attach the source and target labels
        source_label = Gtk.Label("Source")
        source_label.show()
        self.table.attach(source_label, 1, 1+1, 0, 1+0)
        target_label = Gtk.Label("Target")
        target_label.show()
        self.table.attach(target_label, 2, 2+1, 0, 1+0)

    def create_cell(self, text_line_type, text_view_type, row_index, editable):
        cell = Gtk.TextView()
        cell.set_editable(editable)
        cell.set_cursor_visible(False)
        cellTextBuffer = cell.get_buffer()
        index = row_index + self.tables_content[self.table_index]
        cellTextBuffer.set_text(self.tables_content[text_line_type][index].rstrip('\n'))
        self.tables_content[text_view_type][index] = cell
        if self.table_type == "translation_table":
            cellTextBuffer.connect("changed", self.cell_in_translation_table_changed, index)
            if index in self.translation_reference_text_TextViews_modified_flag:
                self.tables_content[self.reference_text_views][index].override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 113, 44, 0.5))

        cell.set_right_margin(20)
        cell.set_wrap_mode(2)#2 == Gtk.WRAP_WORD
        cell.show()
        self.table.attach(cell, text_line_type + 1, text_line_type + 2, row_index + 1, row_index + 2)

    def get_insertion_and_deletions(self, original, modified):
        s = difflib.SequenceMatcher(None, original, modified)
        insertions = []
        deletions = []
        for tag, i1, i2, j1, j2 in s.get_opcodes():
            if tag == "insert" or tag == "replace":insertions.append((j1,j2))
            if tag == "delete"or tag == "replace": deletions.append((i1,i2))
        return (insertions,deletions)


    def create_cells(self):
        for row_index in range (0,self.tables_content[self.rows_ammount]):
            try:
                self.create_cell(self.source_text_lines, self.source_text_views, row_index, False)
                self.create_cell(self.reference_text_lines, self.reference_text_views, row_index, True)
            except IndexError:
                self.next_button.set_visible(False)

    def create_diff(self, text_buffers_array, color):
        for row_index in range (0,self.tables_content[self.rows_ammount]):
            try:
                index = row_index + self.tables_content[self.table_index]
                text_buffer = text_buffers_array[index].get_buffer()

                original = self.tables_content[self.source_text_lines][index]
                modified = self.tables_content[self.reference_text_lines][index]
                insertions,deletions = self.get_insertion_and_deletions(original,modified)
                if color == "green": start = insertions[0][0]; end = insertions[0][1]
                if color == "red": start = deletions[0][0]; end = deletions[0][1]
                self.apply_tag( start, end,text_buffer, color)
            except IndexError: pass

    def create_diffs(self):
        self.create_diff(self.tables_content[self.source_text_views],"red")
        self.create_diff(self.tables_content[self.reference_text_views],"green")

    def _move_in_table(self, ammount_of_lines_to_move, feel_free_to_change_the_buttons = True):
        if not self.tables_content[self.initialized]:
            self.tables_content[self.initialized] = True
            self._fill_table()
        self._clean_table()
        if ammount_of_lines_to_move > 0 or self.tables_content[self.table_index] > 0:
             self.tables_content[self.table_index] += ammount_of_lines_to_move
        if self.tables_content[self.table_index] == 0:
            self.back_button.set_visible(False)
        self.create_cells()
        if self.table_type == "diff_table":
            self.create_diffs()
        if (feel_free_to_change_the_buttons
            and ammount_of_lines_to_move == -1):
            self.next_button.set_visible(True)
        else:
            self.back_button.set_visible(True)

    def _back_in_table(self, button):
        self._move_in_table(-1, self.table_type)
    def _next_in_table(self, button):
        self._move_in_table(+1,self.table_type)
    def _increase_table_rows(self, button):
        self.tables_content[self.rows_ammount] += 1
        self.update_table()
    def _reduce_table_rows(self, button):
        if self.tables_content[self.rows_ammount] > 1:
            self.tables_content[self.rows_ammount] -= 1
            self.update_table()
    def update_table(self, to_change_the_buttons_or_not = False):
        self._move_in_table(+1, to_change_the_buttons_or_not)
        self._move_in_table(-1, to_change_the_buttons_or_not)


    def _search_button_action(self, button, line_index):
        self._move_in_table(line_index - self.tables_content[self.table_index] - 1)
