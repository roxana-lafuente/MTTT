
def combine_and_save_to_index_html():
    header = ""
    footer = ""
    content = ""
    with open ("header.html", 'r') as f:
        header = f.read()

    with open ("footer.html", 'r') as f:
        footer = f.read()

    with open ("content.html", 'r') as f:
        content = f.read()
    filepath_complete = "index.html"
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
    pie_script = get_template("pie_script_template.html")
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
def add_pie_script_to_content(script, content):
    starts_at = contentHTML.rfind("<script")
    content = content[:starts_at] + script + content[starts_at:]
    return content
def save_contentHTML(text):
    text_file = open("content.html", "w")
    text_file.write(text)
    text_file.close()


if __name__ == "__main__":
    #read content.html as an array of lines
    contentHTML_lines = get_template("content_template.html")
    #remove the old pie script
    contentHTML = delete_from_html(contentHTML_lines, "<script", "</script>", True)
    #create new pie script
    json_string = '{label: "Roxana Lafuente", data: 60.07}, {label: "miguelemosreverte", data: 39.93}'
    pie_script = add_json_string_to_pie_script(json_string)
    #add new pie script
    contentHTML = add_pie_script_to_content(pie_script,contentHTML_lines)
    #save_contentHTML
    save_contentHTML(contentHTML)
    combine_and_save_to_index_html()
