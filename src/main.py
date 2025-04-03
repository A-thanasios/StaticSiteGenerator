from leafnode import LeafNode
from parentnode import ParentNode
from converter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, \
    markdown_to_blocks
from src.converter import split_nodes_image, text_to_textnodes, block_to_block_type, markdown_to_html_node
from textnode import TextNode, TextType


def main():
    md4 = """
    ```
This is text that _should_ remain
the **same** even with inline stuff
```
    """
    md = """
    # This is header

    This is **bolded** paragraph

    ```
    This is code
    another code
    ```

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items

    1. This is an ordered list
    2. This is an ordered list too
    3. This is an ordered list too too
    """
    md1 = """
    # This is header 1

    ## This is header 2

    ### This is header 3

    #### This is header 4

    ##### This is header 5

    ###### This is header 6
    """
    md2 = '''
    # This is header 1

    This is paragraph

    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line
    '''

    md3 = '''
    - This is a list
    - with items
    '''




    print(markdown_to_html_node(md4).to_html())

    #print(block + '\n' + str(block_to_block_type(block)))

main()
