from textnode import TextNode, TextType


class HTMLNode:
    def __init__(self, tag: str =None, value: str =None, children: list =None, props: dict =None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ''

        props_str = []
        for key, value in self.props.items():
            props_str.append(f'{key}={value}')

        return ' '.join(props_str)

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'