from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError

        if self.tag is None:
            return self.value

        if self.tag == "a":
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}>"

        return f"<{self.tag}>{self.value}</{self.tag}>"
