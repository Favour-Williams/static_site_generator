from enum import Enum
import re
from inline_markdown import TextNode, TextType, split_nodes_image, split_nodes_link
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    filtered_blocks = []
    
    for block in raw_blocks:
        stripped = block.strip()
        if stripped != "":
            filtered_blocks.append(stripped)
            
    return filtered_blocks


def block_to_block_type(block):
    # Headings: 1-6 # followed by a space
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    
    # Code blocks: Start and end with 3 backticks
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    # Split into lines for multi-line checks
    lines = block.split("\n")
    
    # Quote blocks: Every line starts with >
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                break
        else:
            return BlockType.QUOTE
            
    # Unordered lists: Every line starts with "- "
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                break
        else:
            return BlockType.UNORDERED_LIST
            
    # Ordered lists: Every line starts with "1. ", "2. ", etc.
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                break
            i += 1
        else:
            return BlockType.ORDERED_LIST
            
    # Default fallback
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.HEADING:
        return create_heading_node(block)
    if block_type == BlockType.CODE:
        return create_code_node(block)
    if block_type == BlockType.QUOTE:
        return create_quote_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return create_unordered_list_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return create_ordered_list_node(block)
    return create_paragraph_node(block)

# --- Helper Functions ---

def text_to_children(text):
    """Converts a string of text into a list of HTMLNodes (inline markdown)."""
    # Assuming text_to_textnodes is available in your inline_markdown module
    from inline_markdown import text_to_textnodes
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children

def create_paragraph_node(block):
    # Join lines with a space to handle multi-line paragraphs correctly
    lines = block.split("\n")
    paragraph = " ".join(lines)
    return ParentNode("p", text_to_children(paragraph))

def create_heading_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    # Get text after hashes and the mandatory space
    text = block[level + 1:]
    return ParentNode(f"h{level}", text_to_children(text))

def create_code_node(block):
    # Strip the triple backticks and the newline
    text = block.strip("`").strip("\n")
    # Manual creation of TextNode/HTMLNode to skip inline parsing
    content = text_node_to_html_node(TextNode(text, TextType.TEXT))
    code_node = ParentNode("code", [content])
    return ParentNode("pre", [code_node])

def create_quote_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        # Remove the '>' and strip whitespace
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    return ParentNode("blockquote", text_to_children(content))

def create_unordered_list_node(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        # Strip the "- " (first two chars)
        text = line[2:]
        list_items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", list_items)

def create_ordered_list_node(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        # Strip the "1. " (find first space to handle "10. " etc.)
        first_space = line.find(" ")
        text = line[first_space + 1:]
        list_items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", list_items)

