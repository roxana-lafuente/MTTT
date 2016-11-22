import difflib
import textwrap
import re
import os

class Diff2HTML:

    def __init__(self, user_local_repository_path):
        self.user_local_repository_path = user_local_repository_path

    def prepareHTML(self):
        lines = []
        filtered_lines = []
        with open(self.statistics_html_filepath) as f:
            lines = f.read().splitlines()
        for line in lines:
            if "<thead>" not in line and "</thead>" not in line:
                filtered_lines.append(line)

        final_string = '\n'.join(filtered_lines)
        pat = r'>(\d+)<'
        offset = 0
        for m in re.finditer(pat, '\n'.join(filtered_lines)):
            start = m.start(0) + offset
            end = m.end(0) + offset
            final_string = final_string[:start] + final_string[end:]
            offset -= len (final_string[start:end])

        text_file = open(self.statistics_html_filepath, "w")
        text_file.write(final_string)
        text_file.close()

    def prepare_text_for_HTML_output(self, text):
        text = '\n\n'.join(['\n'.join(textwrap.wrap(line, 40,
                 break_long_words=False, replace_whitespace=False))
                 for line in text.splitlines() if line.strip() != ''])
        return text

    def calculateGitStatistics(self, filename):
        filename = self.user_local_repository_path + filename
        filename_without_extension = os.path.splitext(filename)[0]
        filename_extension = os.path.splitext(filename)[1]

        fromfile = filename
        tofile =  filename_without_extension + "_modified" + filename_extension
        fromlines = open(fromfile, 'U').readlines()
        tolines = open(tofile, 'U').readlines()

        #diff = difflib.HtmlDiff(8,40).make_file(fromlines,tolines,fromfile,tofile)
        diff = difflib.HtmlDiff().make_file(fromlines,tolines,fromfile,tofile)
        self.statistics_html_filepath = self.user_local_repository_path + "/index.html"
        text_file = open(self.statistics_html_filepath, "w")
        text_file.write(diff)
        text_file.close()
        self.prepareHTML()
