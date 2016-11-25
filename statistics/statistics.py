
def combine_and_save_to_index_html():
    header = ""
    footer = ""
    content = ""
    with open ("statistics/header.html", 'r') as f:
        header = f.read()

    with open ("statistics/footer.html", 'r') as f:
        footer = f.read()

    with open ("statistics/content.html", 'r') as f:
        content = f.read()
    filepath_complete = "statistics/index.html"
    text_file = open(filepath_complete, "w")
    text_file.write(header)
    text_file.write(content)
    text_file.write(footer)
    text_file.close()

def get_template(filepath):
    lines = []
    with open (filepath, 'r') as f:
            lines = f.read()
    return lines

def add_json_string_to_pie_script(text):
    #get old pie script
    pie_script = get_template("statistics/pie_script_template.html")
    start_here = pie_script.find("[") + 1
    pie_script = pie_script[:start_here] + text + pie_script[start_here:]
    return pie_script
def delete_from_html(x, contentHTML,b, erase_completly = True):
    start = x.rfind(contentHTML)
    end = x.rfind(b)
    if erase_completly:
        x = x[:start] + x[end + len(b):]
    else:
        x = x[:start + len(contentHTML)] + x[end:]
    return x
def add_pie_script_to_content(script, pie_script):
    starts_at = pie_script.rfind("<script")
    pie_script = pie_script[:starts_at] + script + pie_script[starts_at:]
    return pie_script
def save_contentHTML(text):
    text_file = open("statistics/content.html", "w")
    text_file.write(text)
    text_file.close()

def inject_into_html(pie_as_json_string):
    #read content.html as an array of lines
    contentHTML = get_template("statistics/content_template.html")
    #remove the old pie script
    contentHTML = delete_from_html(contentHTML, "<script", "</script>", True)
    #create new pie script
    pie_script = add_json_string_to_pie_script(pie_as_json_string)
    #add new pie script
    contentHTML = add_pie_script_to_content(pie_script,contentHTML)
    #save_contentHTML
    save_contentHTML(contentHTML)
    combine_and_save_to_index_html()
