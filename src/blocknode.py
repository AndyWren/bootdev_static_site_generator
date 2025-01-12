from enum import Enum
from htmlnode import HTMLNode
import re

from parentnode import ParentNode
from leafnode import LeafNode
from textnode import text_to_children


class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"


class BlockNode:
    def __init__(self, text, block_type):
        self.text = text
        self.block_type = block_type

    def __eq__(self, other):
        return self.text == other.text and self.block_type == other.block_type

    def __repr__(self):
        return f"{self.__class__.__name__}({self.text}, {self.block_type})"


def markdown_to_blocks(markdown):
    result = [l.strip() for l in markdown.split(sep="\n\n") if l]
    return result


def block_to_block_type(block_of_markdown_text):
    match block_of_markdown_text:
        case block_of_markdown_text if re.match(r"^#{1,6} .*$", block_of_markdown_text):
            return BlockType.HEADING
        case block_of_markdown_text if re.findall(
            r"^\s*`{3}(.*?)\n(.*?)^\s*`{3}",
            block_of_markdown_text,
            flags=re.MULTILINE | re.DOTALL,
        ):
            return BlockType.CODE
        case block_of_markdown_text if re.findall(
            r"^>.*$", block_of_markdown_text, flags=re.MULTILINE
        ):
            return BlockType.QUOTE
        case block_of_markdown_text if re.findall(
            r"^(\*|-)\s.*$", block_of_markdown_text, flags=re.MULTILINE
        ):
            return BlockType.UNORDERED_LIST
        case block_of_markdown_text if re.findall(
            r"^\d+\.\s.*$", block_of_markdown_text, flags=re.MULTILINE
        ):
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH


def text_node_to_html_node(block_node):
    match block_node.block_type:
        case BlockType.HEADING:
            return heading_to_html_node(block_node.text)
        case BlockType.CODE:
            return code_to_html_node(block_node.text)
        case BlockType.QUOTE:
            return quote_to_html_node(block_node.text)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block_node.text)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block_node.text)
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block_node.text)
        case _:
            raise Exception("Unknown block type")


def paragraph_to_html_node(text):
    return ParentNode(tag="p", children=text_to_children(text))


def heading_to_html_node(text):
    hash_count = text.count("#")
    texts = text.split(" ", 1)
    return ParentNode(tag=f"h{hash_count}", children=text_to_children(texts[1]))


def code_to_html_node(text):
    bare_text = text.strip("`").strip()
    return ParentNode(tag="pre", children=[LeafNode(tag="code", value=bare_text)])


def quote_to_html_node(text):
    quotes = [quote[2:] for quote in text.split("\n")]
    return LeafNode(tag="blockquote", value=" ".join(quotes))


def unordered_list_to_html_node(text):
    ul = text.split("\n")
    children = [
        ParentNode(tag="li", children=text_to_children(item[2:])) for item in ul
    ]
    return ParentNode(tag="ul", children=children)


def ordered_list_to_html_node(text):
    ol = text.split("\n")
    children = [
        ParentNode(tag="li", children=text_to_children(item.split(". ")[1]))
        for item in ol
    ]
    return ParentNode(tag="ol", children=children)


def markdown_to_html_node(markdown) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    block_nodes = [BlockNode(block, block_to_block_type(block)) for block in blocks]
    page = page_layering(block_nodes)

    return page


def page_layering(block_nodes: list[BlockNode]) -> HTMLNode:
    children = [text_node_to_html_node(block_node) for block_node in block_nodes]
    parent_page = ParentNode(tag="div", children=children)

    return parent_page


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    result = [block[2:] for block in blocks if block.startswith("# ")]

    if not result:
        raise Exception("Title not present")

    return result[0]
