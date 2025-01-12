import unittest

from src.parentnode import ParentNode
from src.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_para(self):
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(expected, node.to_html())

    def test_href(self):
        expected = '<p><b>Bold text</b>Normal text<i>italic text</i><a href="https://www.google.com">Click me!</a></p>'
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode("a", "Click me!", {"href": "https://www.google.com"}),
            ],
        )
        self.assertEqual(expected, node.to_html())

    def test_parent_of_parent(self):
        expected = '<p><p><b>Bold text</b>Normal text<i>italic text</i><a href="https://www.google.com">Click me!</a></p></p>'
        node = ParentNode(
            "p",
            children=[
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode("a", "Click me!", {"href": "https://www.google.com"}),
                    ],
                )
            ],
        )
        self.assertEqual(expected, node.to_html())
