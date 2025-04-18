import unittest

from converter import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, split_nodes_image, \
    split_nodes_link, markdown_to_blocks, markdown_to_html_node
from textnode import TextNode, TextType


class TestConverter(unittest.TestCase):

    # Test cases for text_node_to_html_node(text_node)
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is a italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This.com/is/a/link/node", TextType.LINK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This.com/is/a/link/node")
        self.assertEqual(html_node.props, {'href': "This.com/is/a/link/node"})

    def test_image(self):
        node = TextNode("This is a image node", TextType.IMAGE, "This/is/a/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props, {'src': "This/is/a/image.png",
                                           'alt': "This is a image node"})

    # Test cases for split_nodes_delimiter(old_nodes, delimiter, text_type)

    def test_split_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "This is a text node")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_split_with_bold_delimiter(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is text with a ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " word")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_split_with_italic_delimiter(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is text with a ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text, " word")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_split_with_code_delimiter(self):
        node = TextNode("This is text with a `code` word", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is text with a ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "code")
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text, " word")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_multiple_delimiters(self):
        node = TextNode("This has **multiple** bold **words** in it", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].text, "This has ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "multiple")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " bold ")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text, "words")
        self.assertEqual(nodes[3].text_type, TextType.BOLD)
        self.assertEqual(nodes[4].text, " in it")
        self.assertEqual(nodes[4].text_type, TextType.TEXT)

    def test_odd_delimiters(self):
        node = TextNode("This has an odd **number of delimiters", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_different_delimiters(self):
        # First, test bold delimiter
        node = TextNode("Text with **bold** and `code` and _italic_", TextType.TEXT)

        # Process bold first
        bold_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(bold_nodes), 3)
        self.assertEqual(bold_nodes[0].text, "Text with ")
        self.assertEqual(bold_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(bold_nodes[1].text, "bold")
        self.assertEqual(bold_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(bold_nodes[2].text, " and `code` and _italic_")
        self.assertEqual(bold_nodes[2].text_type, TextType.TEXT)

        # Then process code in the result from bold processing
        code_nodes = split_nodes_delimiter(bold_nodes, "`", TextType.CODE)
        self.assertEqual(len(code_nodes), 5)
        self.assertEqual(code_nodes[0].text, "Text with ")
        self.assertEqual(code_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(code_nodes[1].text, "bold")
        self.assertEqual(code_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(code_nodes[2].text, " and ")
        self.assertEqual(code_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(code_nodes[3].text, "code")
        self.assertEqual(code_nodes[3].text_type, TextType.CODE)
        self.assertEqual(code_nodes[4].text, " and _italic_")
        self.assertEqual(code_nodes[4].text_type, TextType.TEXT)

        # Finally process italic in the result from code processing
        italic_nodes = split_nodes_delimiter(code_nodes, "_", TextType.ITALIC)
        self.assertEqual(len(italic_nodes), 6)
        self.assertEqual(italic_nodes[0].text, "Text with ")
        self.assertEqual(italic_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(italic_nodes[1].text, "bold")
        self.assertEqual(italic_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(italic_nodes[2].text, " and ")
        self.assertEqual(italic_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(italic_nodes[3].text, "code")
        self.assertEqual(italic_nodes[3].text_type, TextType.CODE)
        self.assertEqual(italic_nodes[4].text, " and ")
        self.assertEqual(italic_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(italic_nodes[5].text, "italic")
        self.assertEqual(italic_nodes[5].text_type, TextType.ITALIC)

    def test_different_delimiters_asynch(self):
        node = TextNode("Text with **bold** and _italic_ and `code`", TextType.TEXT)

        # Process bold
        bold_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(bold_nodes), 3)
        self.assertEqual(bold_nodes[0].text, "Text with ")
        self.assertEqual(bold_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(bold_nodes[1].text, "bold")
        self.assertEqual(bold_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(bold_nodes[2].text, " and _italic_ and `code`")
        self.assertEqual(bold_nodes[2].text_type, TextType.TEXT)

        # Process code
        code_nodes = split_nodes_delimiter(bold_nodes, "`", TextType.CODE)
        self.assertEqual(len(code_nodes), 4)
        self.assertEqual(code_nodes[0].text, "Text with ")
        self.assertEqual(code_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(code_nodes[1].text, "bold")
        self.assertEqual(code_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(code_nodes[2].text, " and _italic_ and ")
        self.assertEqual(code_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(code_nodes[3].text, "code")
        self.assertEqual(code_nodes[3].text_type, TextType.CODE)

        # Process italic
        italic_nodes = split_nodes_delimiter(code_nodes, "_", TextType.ITALIC)
        self.assertEqual(len(italic_nodes), 6)
        self.assertEqual(italic_nodes[0].text, "Text with ")
        self.assertEqual(italic_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(italic_nodes[1].text, "bold")
        self.assertEqual(italic_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(italic_nodes[2].text, " and ")
        self.assertEqual(italic_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(italic_nodes[3].text, "italic")
        self.assertEqual(italic_nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(italic_nodes[4].text, " and ")
        self.assertEqual(italic_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(italic_nodes[5].text, "code")
        self.assertEqual(italic_nodes[5].text_type, TextType.CODE)

    def test_multiple_nodes(self):
        # Create a list with multiple nodes of different types
        nodes = [
            TextNode("This is **bold** text", TextType.TEXT),
            TextNode("This is already italic", TextType.ITALIC),
            TextNode("And this has `code`", TextType.TEXT)
        ]

        # Process bold first
        bold_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(bold_nodes), 5)
        self.assertEqual(bold_nodes[0].text, "This is ")
        self.assertEqual(bold_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(bold_nodes[1].text, "bold")
        self.assertEqual(bold_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(bold_nodes[2].text, " text")
        self.assertEqual(bold_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(bold_nodes[3].text, "This is already italic")
        self.assertEqual(bold_nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(bold_nodes[4].text, "And this has `code`")
        self.assertEqual(bold_nodes[4].text_type, TextType.TEXT)

        # Then process code
        code_nodes = split_nodes_delimiter(bold_nodes, "`", TextType.CODE)
        self.assertEqual(len(code_nodes), 6)
        self.assertEqual(code_nodes[0].text, "This is ")
        self.assertEqual(code_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(code_nodes[1].text, "bold")
        self.assertEqual(code_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(code_nodes[2].text, " text")
        self.assertEqual(code_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(code_nodes[3].text, "This is already italic")
        self.assertEqual(code_nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(code_nodes[4].text, "And this has ")
        self.assertEqual(code_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(code_nodes[5].text, "code")
        self.assertEqual(code_nodes[5].text_type, TextType.CODE)

        # Finally, process italic
        italic_nodes = split_nodes_delimiter(code_nodes, "_", TextType.ITALIC)
        self.assertEqual(len(italic_nodes), 6)
        self.assertEqual(italic_nodes[0].text, "This is ")
        self.assertEqual(italic_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(italic_nodes[1].text, "bold")
        self.assertEqual(italic_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(italic_nodes[2].text, " text")
        self.assertEqual(italic_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(italic_nodes[3].text, "This is already italic")
        self.assertEqual(italic_nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(italic_nodes[4].text, "And this has ")
        self.assertEqual(italic_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(italic_nodes[5].text, "code")
        self.assertEqual(italic_nodes[5].text_type, TextType.CODE)

        # Test cases for extract_markdown_images(text)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        # Test cases for extract_markdown_links(text)

            #TODO:

        # Test cases for split_nodes_images([node])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    # To blocks

    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here This is the same paragraph on a new line",
                "- This is a list - with items",
            ],
        )

    # markdown_to_html_node

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here
    
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )