from textnode import TextNode, TextType
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        parts = node.text.split(delimiter)
        
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid Markdown: matching delimiter '{delimiter}' not found.")
        
        node_parts = []
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                node_parts.append(TextNode(parts[i], TextType.TEXT))
            else:
                node_parts.append(TextNode(parts[i], text_type))
        
        new_nodes.extend(node_parts)
        
    return new_nodes

def extract_markdown_images(text):
    import re
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    import re
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        
        last_index = 0
        for alt, url in matches:
            start_index = node.text.find(f"![{alt}]({url})", last_index)
            if start_index == -1:
                continue
            
            if start_index > last_index:
                new_nodes.append(TextNode(node.text[last_index:start_index], TextType.TEXT))
            
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            last_index = start_index + len(f"![{alt}]({url})")
        
        if last_index < len(node.text):
            new_nodes.append(TextNode(node.text[last_index:], TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue
        
        last_index = 0
        for anchor, url in matches:
            start_index = node.text.find(f"[{anchor}]({url})", last_index)
            if start_index == -1:
                continue
            
            if start_index > last_index:
                new_nodes.append(TextNode(node.text[last_index:start_index], TextType.TEXT))
            
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            last_index = start_index + len(f"[{anchor}]({url})")
        
        if last_index < len(node.text):
            new_nodes.append(TextNode(node.text[last_index:], TextType.TEXT))
    
    return new_nodes
