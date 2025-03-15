from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict =None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode has no value")

        if self.tag is None:
            return self.value
        if self.props is not None:
            return (f'<{self.tag} '
                    f'{' '.join([f'{key}="{value}"' for key, value in self.props.items()])}>'                                              
                    f'{self.value}</{self.tag}>')
        else:
            return f'<{self.tag }>{self.value}</{self.tag}>'