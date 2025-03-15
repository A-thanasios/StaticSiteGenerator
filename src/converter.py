from leafnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception('Not valid text type')

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code', text_node.text)
        case TextType.LINK:
            return LeafNode('a', text_node.text, {'href': text_node.text})
        case TextType.IMAGE:
            return LeafNode('img', '',  {'src': text_node.url, 'alt': text_node.text})
        case _:
            raise Exception('Not valid text type')