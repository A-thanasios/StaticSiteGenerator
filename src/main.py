from leafnode import LeafNode
from parentnode import ParentNode
from converter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, \
    markdown_to_blocks
from src.converter import split_nodes_image, text_to_textnodes, block_to_block_type
from textnode import TextNode, TextType


def main():
    md = """
    This is **bolded** paragraph

    ```This is code```

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items

    1. This is an ordered list
    2. This is an ordered list too
    3bootdev run 719ee1ae-19b6-4572-9b40-c8530dcbfa4f -s. This is an ordered list too too
    """
    blocks = markdown_to_blocks(md)
    block = blocks[-1]



    for block in blocks:
        print(block + '\n' + str(block_to_block_type(block)) + '\n')

    #print(block + '\n' + str(block_to_block_type(block)))

main()
