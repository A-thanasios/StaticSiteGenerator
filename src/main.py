from leafnode import LeafNode
from parentnode import ParentNode
from converter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link
from src.converter import split_nodes_image, text_to_textnodes
from textnode import TextNode, TextType


def main():
    text_node = TextNode('This is text with a **bolded phrase** in the middle',
                         TextType.TEXT,
                         )


    node = TextNode(
    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
    TextType.TEXT,
    )
#print(extract_markdown_images(text))
# [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

#print(split_nodes_image([node]))
# [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

    text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'

    print(text_to_textnodes(text))
main()
