from textnode import TextNode, TextType


def main():
    text_node = TextNode('sds',
                         TextType.bold_text,
                         'https://www.oimahbalfs.org' )

    print(text_node.__repr__())


main()
