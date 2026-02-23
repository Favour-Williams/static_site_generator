from gencontent import extract_title

import unittest

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
        self.assertEqual(extract_title("#  Welcome Home  "), "Welcome Home")
        
    def test_extract_title_fail(self):
        with self.assertRaises(Exception):
            extract_title("## This is an h2")
        with self.assertRaises(Exception):
            extract_title("No header here")
