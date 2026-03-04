import os
import shutil
from copystatic import copy_files_recursive
from gencontent import generate_page, generate_pages_recursive

from textnode import TextNode, TextType
def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    copy_files_recursive("./static", "./public")
    
    # 2. Generate Index Page
    generate_pages_recursive("content", "template.html", "public")
if __name__ == "__main__":
    main()