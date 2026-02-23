import os
import shutil
from copystatic import copy_files_recursive
from gencontent import generate_page

from textnode import TextNode, TextType
def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    copy_files_recursive("./static", "./public")
    
    # 2. Generate Index Page
    generate_page(
        "content/index.md", 
        "template.html", 
        "public/index.html"
    )
if __name__ == "__main__":
    main()