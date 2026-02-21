from inline_markdown import split_nodes_delimiter
import unittest
from textnode import TextNode, TextType
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_unmatched(self):
        nodes = [TextNode("This is **bold text", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com)"
        matches = extract_markdown_images(text)
        expected = [
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("another", "https://i.imgur.com")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_links_no_images(self):
        # Ensure that images are NOT captured by the link extractor
        text = "This is an image ![alt](url) and this is a link [anchor](url)"
        matches = extract_markdown_links(text)
        expected = [("anchor", "url")]
        self.assertListEqual(expected, matches)

    def test_extract_images_no_links(self):
        # Ensure that links are NOT captured by the image extractor
        text = "This is an image ![alt](url) and this is a link [anchor](url)"
        matches = extract_markdown_images(text)
        expected = [("alt", "url")]
        self.assertListEqual(expected, matches)