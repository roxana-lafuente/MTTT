# a very C reminicent style, lets see how it plays out! here's hope they dont tell me to rewrite it
def combine_and_save_to_html(filename):
    header = ""
    footer = ""
    content = ""
    with open ("statistics/header.html", 'r') as f:
        header = f.read()

    with open ("statistics/footer.html", 'r') as f:
        footer = f.read()

    with open ("statistics/generated/content.html", 'r') as f:
        content = f.read()
    filepath_complete = "statistics/generated/" + filename + ".html"
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
def add_at(at, to_add, contentHTML):
    starts_at = contentHTML.rfind(at)
    contentHTML = contentHTML[:starts_at] + to_add + contentHTML[starts_at:]
    return contentHTML
def save_contentHTML(text):
    text_file = open("statistics/generated/content.html", "w")
    text_file.write(text)
    text_file.close()

def inject_into_html(pie_as_json_string, table_data, table_title, filename):
    #read content.html as an array of lines
    contentHTML = get_template("statistics/content_template.html")

    contentHTML = add_at("<!--table title ends here. ",
        table_title, contentHTML)
    contentHTML = add_at("<!--pie script starts here. ",
        add_json_string_to_pie_script(pie_as_json_string), contentHTML)
    contentHTML = add_at("<!--table data input ends here. ",
        table_data, contentHTML)

    save_contentHTML(contentHTML)
    combine_and_save_to_html(filename)
