class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        return " " + " ".join(f'{k}="{v}"' for k, v in self.props.items())

    def __repr__(self):
        return f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"

    def __eq__(self, other):
        if isinstance(other, HTMLNode):
            return (
                self.tag == other.tag
                and self.value == other.value
                and self.children == other.children
                and self.props == other.props
            )
        return False
