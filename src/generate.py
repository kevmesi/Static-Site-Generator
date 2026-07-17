from blockshare import markdown_to_html_node, extract_title
import os

template_title = r"{{ Title }}"
template_content = r"{{ Content }}"

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    
    print("Generating page from", from_path, "to", dest_path, "using", template_path)

    with open(from_path) as m:
        markdown = m.read()
    with open(template_path) as t:
        template = t.read()

    page_title = extract_title(markdown)
    page_content = markdown_to_html_node(markdown).to_html()

    page = template.replace(template_title, page_title).replace(template_content, page_content)

    check_destination(dest_path)

    with open(dest_path, "wt") as dest:
        dest.write(page)


def check_destination(path: str) -> None:

    path_split = path.split("/")
    dirs_path = "/".join(path_split[:-1])

    if not os.path.exists(dirs_path):
        os.makedirs(dirs_path)


