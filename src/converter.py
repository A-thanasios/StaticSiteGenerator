import  re
from leafnode import LeafNode
from textnode import TextNode, TextType


def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')


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

def text_to_textnodes(text):
    lst = [TextNode(text, TextType.TEXT)]

    lst = (split_nodes_delimiter(lst, '**', TextType.BOLD))
    lst = (split_nodes_delimiter(lst, '_', TextType.ITALIC))
    lst = (split_nodes_delimiter(lst, '`', TextType.CODE))
    lst = (split_nodes_image(lst))
    lst = (split_nodes_link(lst))

    return lst
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

def extract_markdown_images(text :str):
    return re.findall(r'!\[(.*?)\]\((.*?)\)', text)


def extract_markdown_links(text :str):
    return re.findall(r'\[(.*?)\]\((.*?)\)', text)

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        images_tuple = extract_markdown_images(old_node.text)

        if len(images_tuple) == 0:
            new_nodes.append(old_node)
            continue

        rest = old_node.text
        while len(images_tuple) > 0:

            before, rest = rest.split(f'![{images_tuple[0][0]}]({images_tuple[0][1]})', 1)
            new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(images_tuple[0][0], TextType.IMAGE, images_tuple[0][1]))

            images_tuple.remove(images_tuple[0])


    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links_tuple = extract_markdown_links(old_node.text)


        if len(links_tuple) == 0:
            new_nodes.append(old_node)
            continue

        rest = old_node.text
        while len(links_tuple) > 0:

            before, rest = rest.split(f'[{links_tuple[0][0]}]({links_tuple[0][1]})', 1)
            new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(links_tuple[0][0], TextType.LINK, links_tuple[0][1]))

            links_tuple.remove(links_tuple[0])


    return new_nodes