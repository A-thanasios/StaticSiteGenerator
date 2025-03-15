from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict =None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode has no tag")
        if not self.children:
            raise ValueError("ParentNode has no children")
        node = f'<{self.tag}>'
        for child in self.children:
            node += child.to_html()
        else:
            node += f'</{self.tag}>'
        return node