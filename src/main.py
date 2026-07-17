import os
import shutil

from copystatic import copy_files_recursive
from generate import generate_page

dir_path_static = "./static"
dir_path_public = "./public"

file_path_template = "template.html"
file_path_source = "./content/index.md"
file_path_dest = "./public/index.html"


def main() -> None:
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    generate_page(file_path_source, file_path_template, file_path_dest)


main()