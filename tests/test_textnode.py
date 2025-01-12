import unittest

from src.textnode import (
    TextNode,
    TextType,
    TextTypePatterns,
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown,
    split_nodes_link,
    split_nodes_image,
    text_to_textnodes,
)
from src.leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, url="https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, url="https://boot.dev")
        self.assertEqual(node, node2)

    def test_eq_short(self):
        node = TextNode("T", TextType.BOLD, url="h")
        node2 = TextNode("T", TextType.BOLD, url="h")
        self.assertEqual(node, node2)

    def test_not_eq_from_url(self):
        node = TextNode("This is a text node", TextType.BOLD, url="https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_from_text(self):
        node = TextNode("A", TextType.BOLD)
        node2 = TextNode("B", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_from_text_type(self):
        node = TextNode("A", TextType.BOLD)
        node2 = TextNode("A", TextType.TEXT)
        self.assertNotEqual(node, node2)


class TestTextNodeConversion(unittest.TestCase):
    def test_normal_conv(self):
        expected = LeafNode(tag=None, value="text")
        node = TextNode("text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(expected, html_node)

    def test_bold_conv(self):
        expected = LeafNode(tag="b", value="bold")
        node = TextNode("bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(expected, html_node)

    def test_link_conv(self):
        expected = LeafNode(tag="a", value="anchor", props={"href": "https://boot.dev"})
        node = TextNode("anchor", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(expected, html_node)

    def test_image_conv(self):
        expected = LeafNode(
            tag="img", value="", props={"src": "https://boot.dev", "alt": "image"}
        )
        node = TextNode("image", TextType.IMAGE, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(expected, html_node)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delimiter(self):
        expected = [
            TextNode("This is text with a ", TextType.TEXT, None),
            TextNode("code block", TextType.CODE, None),
            TextNode(" word", TextType.TEXT, None),
        ]
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(expected, new_nodes)

    def test_bold_delimiter(self):
        expected = [
            TextNode("This is text with a ", TextType.TEXT, None),
            TextNode("bolded phrase", TextType.BOLD, None),
            TextNode(" in the middle", TextType.TEXT, None),
        ]
        node = TextNode(
            "This is text with a **bolded phrase** in the middle", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(expected, new_nodes)

    def test_bold_not_present(self):
        expected = [
            TextNode("This is text with a phrase in the middle", TextType.TEXT, None)
        ]
        node = TextNode("This is text with a phrase in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(expected, new_nodes)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_images(self):
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown(TextTypePatterns.IMAGE.value, text)
        self.assertEqual(expected, result)

    def test_no_images(self):
        expected = []
        self.assertEqual(
            expected, extract_markdown(TextTypePatterns.IMAGE.value, "This is a test!")
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_links(self):
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown(TextTypePatterns.LINK.value, text)
        self.assertEqual(expected, result)

    def test_no_links(self):
        expected = []
        self.assertEqual(
            expected, extract_markdown(TextTypePatterns.LINK.value, "This is a test!")
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertEqual(expected, result)


class TestSplitImagesLink(unittest.TestCase):
    def test_split_images_link(self):
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(", the end!", TextType.TEXT),
        ]
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg), the end!",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertEqual(expected, result)

    def test_split_images_link_no_text_after(self):
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertEqual(expected, result)

    def test_only_image_text(self):
        expected = [
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif")
        ]
        node = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(expected, result)


class TestTextToTextnodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertEqual(expected, result)

    def test_double_bold(self):
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("bold twice", TextType.BOLD),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        text = "This is **text** with an **bold twice** word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
