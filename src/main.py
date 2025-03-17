from leafnode import LeafNode
from parentnode import ParentNode
from converter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


def main():
    text_node = TextNode('This is text with a **bolded phrase** in the middle',
                         TextType.TEXT,
                         )


text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
#print(extract_markdown_images((text,)))
# [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
print(extract_markdown_links((text,)))
# [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
main()
