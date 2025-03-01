from enum import Enum
from leafnode import LeafNode
import re


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextTypePatterns(Enum):
    BOLD = r"\*{2}([^*]+?)\*{2}"
    ITALIC = r"_([^_]+?)_"
    CODE = r"`([^*]+?)`"
    LINK = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    IMAGE = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"{self.__class__.__name__}({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise Exception("Unknown text type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    results = []
    for node in old_nodes:
        results.extend(split_node_delimiter(node, delimiter, text_type))
    return results


def split_node_delimiter(old_node, delimiter, text_type):
    result = []

    texts = old_node.text.split(delimiter)
    if len(texts) == 1:
        return [old_node]

    if texts and (text := texts[0]) and len(text) > 0:
        result.append(TextNode(text, old_node.text_type))
    result.append(TextNode(texts[1], text_type))
    if texts and (text := texts[2]) and len(text) > 0:
        result.append(TextNode(text, old_node.text_type))

    return result


def split_nodes_image(old_nodes):
    results = []
    for node in old_nodes:
        results.extend(split_node_image(node))
    return results


def split_node_image(node):
    original_text = node.text
    extracted = extract_markdown(TextTypePatterns.IMAGE.value, original_text)
    if not extracted:
        return [node]

    results = []

    for image_alt, image_link in extracted:
        sections = original_text.split(f"![{image_alt}]({image_link})", 1)
        if sections[0] is not None and len(sections[0]) > 0:
            results.append(TextNode(sections[0], TextType.TEXT))
        results.append(TextNode(image_alt, TextType.IMAGE, image_link))
        if sections[1] is not None and len(sections[1]) > 0:
            original_text = sections[1]
        else:
            original_text = None

    if original_text:
        results.append(TextNode(original_text, TextType.TEXT))

    return results


def split_nodes_link(old_nodes):
    results = []
    for node in old_nodes:
        results.extend(split_node_link(node))
    return results


def split_node_link(node):
    original_text = node.text
    extracted = extract_markdown(TextTypePatterns.LINK.value, original_text)
    if not extracted:
        return [node]

    results = []

    for image_alt, image_link in extracted:
        sections = original_text.split(f"[{image_alt}]({image_link})", 1)
        if sections[0] is not None and len(sections[0]) > 0:
            results.append(TextNode(sections[0], TextType.TEXT))
        results.append(TextNode(image_alt, TextType.LINK, image_link))
        if sections[1] is not None and len(sections[1]) > 0:
            original_text = sections[1]
        else:
            original_text = None

    if original_text:
        results.append(TextNode(original_text, TextType.TEXT))

    return results


def extract_markdown(pattern: str, text: str) -> list[str]:
    matches = re.findall(pattern, text)
    return matches


def split_nodes(
    nodes: list[TextNode], delimiter: str, text_type: TextType, pattern: str
):
    def split_node(node: TextNode, delimiter: str, text_type: TextType, pattern: str):
        original_text = node.text
        extracted = extract_markdown(pattern, original_text)
        if not extracted:
            return [node]

        r = []

        for split_value in extracted:
            sections = original_text.split(f"{delimiter}{split_value}{delimiter}", 1)
            if sections and (section := sections[0]) and len(section) > 0:
                r.append(TextNode(section, TextType.TEXT))
            r.append(TextNode(split_value, text_type))
            original_text = sections[1]

        if original_text:
            r.append(TextNode(original_text, TextType.TEXT))

        return r

    results = []
    for node in nodes:
        results.extend(split_node(node, delimiter, text_type, pattern))
    return results


def text_to_textnodes(text: str):

    node = TextNode(
        text,
        TextType.TEXT,
    )
    n = split_nodes([node], "**", TextType.BOLD, TextTypePatterns.BOLD.value)
    n = split_nodes(n, "_", TextType.ITALIC, TextTypePatterns.ITALIC.value)
    n = split_nodes(n, "`", TextType.CODE, TextTypePatterns.CODE.value)
    n = split_nodes_image(n)
    n = split_nodes_link(n)
    return n


def text_to_children(text: str) -> list[LeafNode]:
    return [text_node_to_html_node(text_node) for text_node in text_to_textnodes(text)]
