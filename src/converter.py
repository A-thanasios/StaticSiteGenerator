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
            raise Exception(f'"{text_node.text_type}" is not valid text type')

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        if old_node.text.find(delimiter) == -1:
            new_nodes.append(old_node)
            continue

        if old_node.text.count(delimiter) % 2 != 0:
            raise Exception(f'"{delimiter}" not in correct format. '
                            f'Make sure, that desired text is between two {delimiter}.')

        remaining_text = old_node.text
        text_nodes = []

        while delimiter in remaining_text:
            before, rest = remaining_text.split(delimiter, 1)

            if before:
                text_nodes.append(TextNode(before, TextType.TEXT))

            middle, remaining_text = rest.split(delimiter, 1)
            text_nodes.append(TextNode(middle, text_type))

        if remaining_text:
            text_nodes.append(TextNode(remaining_text, TextType.TEXT))

        new_nodes.extend(text_nodes)

    return new_nodes