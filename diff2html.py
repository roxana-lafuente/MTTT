import difflib
import textwrap
import re
import os

class Diff2HTML:

    def __init__(self, saved_absolute_path):
        self.saved_absolute_path = saved_absolute_path

    def calculateGitStatistics(self, filename):
        filename = self.saved_absolute_path + filename
        filename_without_extension = os.path.splitext(filename)[0]
        filename_extension = os.path.splitext(filename)[1]

        fromfile = filename
        tofile =  filename_without_extension + "_modified" + filename_extension
        fromlines = open(fromfile, 'U').readlines()
        tolines = open(tofile, 'U').readlines()

        #diff = difflib.HtmlDiff(8,40).make_file(fromlines,tolines,fromfile,tofile)
        diff = difflib.HtmlDiff().make_file(fromlines,tolines,fromfile,tofile)
        self.statistics_html_filepath = self.saved_absolute_path + "/index.html"
        text_file = open(self.statistics_html_filepath, "w")
        text_file.write(diff)
        text_file.close()
        self.prepareHTML()
