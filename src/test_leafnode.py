import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_link(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "I am heading 1")
        self.assertEqual(node.to_html(), "<h1>I am heading 1</h1>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "I am heading 1")
        self.assertEqual(node.to_html(), "I am heading 1")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("h1", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_empty_string(self):
        node = LeafNode("h1", '')
        with self.assertRaises(ValueError):
            node.to_html()
