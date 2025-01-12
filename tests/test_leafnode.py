import unittest

from src.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_para(self):
        expected = "<p>This is a paragraph of text.</p>"
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(expected, node.to_html())

    def test_href(self):
        expected = '<a href="https://www.google.com">Click me!</a>'
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(expected, node.to_html())

    def test_link(self):
        expected = '<img src="https://i.imgur.com/aKaOqIh.gif" alt="rick roll">'
        node = LeafNode(
            "img",
            "",
            props={"src": "https://i.imgur.com/aKaOqIh.gif", "alt": "rick roll"},
        )
        self.assertEqual(expected, node.to_html())
