from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType


def main():
    text_node = TextNode('sds',
                         TextType.bold_text,
                         'https://www.oimahbalfs.org' )

    grandchild1 = LeafNode("b", "Bold text")
    grandchild2 = LeafNode(None, "Normal text")
    grandchild3 = LeafNode("i", "italic text")
    grandchild4 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    child1 = ParentNode("div", [grandchild1, grandchild2, grandchild3, grandchild4])
    child2 = LeafNode("p", "Hello, world!")
    child3 = ParentNode("div", [child1])
    parent_node = ParentNode("div", [child1, child2, child3])

    print(parent_node.to_html())


main()
