import unittest

from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_has_leading_space(self):
        node = HTMLNode(tag="P", value="Frank", children=["A"], props={"B": "C"})
        self.assertEqual(node.props_to_html()[0], " ")

    def test_is_string(self):
        node = HTMLNode(tag="P", value="Frank", children=["A"], props={"B": "C"})
        self.assertIsInstance(node.props_to_html(), str)

    def test_does_contain(self):
        node = HTMLNode(
            tag="P", value="Frank", children=["A"], props={"B": "C", "D": "E"}
        )
        self.assertIn("B", node.props)
