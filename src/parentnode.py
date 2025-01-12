from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError

        if self.children is None:
            raise ValueError

        child = "".join(c.to_html() for c in self.children)
        return f"<{self.tag}>{child}</{self.tag}>"
