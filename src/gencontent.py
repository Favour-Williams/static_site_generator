import os
from markdown_blocks import *
from copystatic import copy_files_recursive
from htmlnode import HTMLNode, LeafNode, ParentNode

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header found in markdown")

    
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    title = extract_title(markdown_content)
    
    # Replace placeholders
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    
    # Replace root-relative paths with the basepath
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')
    
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "" and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    with open(dest_path, 'w') as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)

        if os.path.isfile(from_path):
            if filename.endswith(".md"):
                dest_html_path = dest_path.replace(".md", ".html")
                # Pass basepath here too!
                generate_page(from_path, template_path, dest_html_path, basepath)
        else:
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            generate_pages_recursive(from_path, template_path, dest_path, basepath)

