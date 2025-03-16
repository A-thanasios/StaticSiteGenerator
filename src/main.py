from leafnode import LeafNode
from parentnode import ParentNode
from src.converter import split_nodes_delimiter
from textnode import TextNode, TextType


def main():
    text_node = TextNode('This is text with a **bolded phrase** in the middle',
                         TextType.TEXT,
                         )


    #print(split_nodes_delimiter([text_node], '**', text_node.text_type))

    print(TextType.get_text_type('**'))


main()
