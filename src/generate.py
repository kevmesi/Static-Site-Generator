from blockshare import markdown_to_html_node, extract_title
import os
from pathlib import Path
from blockshare import markdown_to_html_node

template_title = r"{{ Title }}"
template_content = r"{{ Content }}"



def generate_pages_recursive(
        dir_path_content: str, 
        template_path: str, 
        dest_dir_path: str, 
        basepath: str) -> None:

    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)


def generate_page(from_path: str, template_path: str, dest_path: str | Path, basepath: str) -> None:
    print("Generating page from", from_path, "to", dest_path, "using", template_path)

    with open(from_path) as m:
        markdown = m.read()
    with open(template_path) as t:
        template = t.read()

    page_title = extract_title(markdown)
    page_content = markdown_to_html_node(markdown).to_html()

    page = template.replace(template_title, page_title)\
        .replace(template_content, page_content)\
        .replace('href="/', 'href="' + basepath)\
        .replace('src="/', 'src="' + basepath)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "wt") as dest:
        dest.write(page)



