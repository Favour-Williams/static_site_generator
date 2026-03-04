import os
import shutil
import sys
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

def main():
    # 1. Handle basepath from CLI arguments
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    # 2. Switch from public to docs
    dest_dir = "./docs"
    
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    
    # Copy static assets to docs
    copy_files_recursive("./static", dest_dir)
    
    # Generate pages to docs
    generate_pages_recursive(
        "content", 
        "template.html", 
        dest_dir,
        basepath 
    )

if __name__ == "__main__":
    main()