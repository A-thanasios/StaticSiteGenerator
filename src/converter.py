import  re
from enum import Enum
from unittest import case

from uaclient.daemon import cleanup

from leafnode import LeafNode
from htmlnode import HTMLNode
from parentnode import ParentNode
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


def markdown_to_html_node(markdown):
    htmlnodes = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)


        html_block = block_to_htmlnode(block, block_type)

        htmlnodes.append(html_block)

    return ParentNode('div', htmlnodes)

def text_to_children(text):
    children = []
    textnodes = text_to_textnodes(text)
    for textnode in textnodes:
        children.append(text_node_to_html_node(textnode))
    

    return children


def block_to_htmlnode(text, block_type):

    match block_type:
        case BlockType.HEADING:
            markdown, clean_text = text.split(' ', 1)
            level = len(markdown)
            return ParentNode(f'h{level}', text_to_children(clean_text))

        case BlockType.QUOTE:
            markdown, clean_text = text.split(' ', 1)
            return ParentNode('blockquote', text_to_children(clean_text))

        case BlockType.UNORDERED_LIST:
            markdown, clean_text = text.split(' ', 1)
            nodes = []
            for child in clean_text.split('\n- '):
                nodes.append(LeafNode('li', child))
            return ParentNode('ul', nodes)

        case BlockType.ORDERED_LIST:
            nodes = []
            for child in text.split('\n'):
                nodes.append(LeafNode('li', child.split('. ', 1)[1]))
            return ParentNode('ol', nodes)

        case BlockType.PARAGRAPH:
            return ParentNode('p', text_to_children(text))

        case BlockType.CODE:
            return ParentNode('pre', [text_node_to_html_node(TextNode(text.split('```', 2)[1].lstrip('\n'), TextType.CODE))])


def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    new_blocks = []

    for block in blocks:
        block = block.strip()  # Always strip any leading/trailing whitespace

        if block_to_block_type(block) == BlockType.CODE:
            new_blocks.append(block)
            continue

        # Process non-code blocks
        lines = block.split('\n')
        cleaned_lines = [line.strip() for line in lines if line.strip()]  # Remove empty lines
        new_block = ' '.join(cleaned_lines)  # Concatenate cleaned lines

        if new_block:
            new_blocks.append(new_block)

    return new_blocks

def block_to_block_type(block):
    if  block[0] == '#':
        return BlockType.HEADING
    elif block[0:3] and block [-3:] == '```':
        return BlockType.CODE
    elif block[0] == '>':
        for line in block:
            if line != '>':
                continue
        return BlockType.QUOTE
    elif block[0] == '-':
        for line in block.split('\n'):
            if line[0] != '-':
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block[0].isdigit() and block[1] == '.':
        n = 1
        for line in block.split('\n'):
            if not line[0].isdigit() or line[1] != '.' or line[0] != f'{n}':
                return BlockType.PARAGRAPH
            n += 1

        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


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