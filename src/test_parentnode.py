import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_multi_children(self):
        child1 = LeafNode("b", "Bold text")
        child2 = LeafNode(None, "Normal text")
        child3 = LeafNode("i", "italic text")
        child4 = LeafNode(None, "Normal text")
        parent_node = ParentNode("div", [child1, child2, child3, child4])
        self.assertEqual(parent_node.to_html(),
        '<div><b>Bold text</b>Normal text<i>italic text</i>Normal text</div>')

    def test_to_html_multi_children_with_link(self):
        child1 = LeafNode("b", "Bold text")
        child2 = LeafNode(None, "Normal text")
        child3 = LeafNode("i", "italic text")
        child4 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child1, child2, child3, child4])
        self.assertEqual(parent_node.to_html(),
        '<div><b>Bold text</b>Normal text<i>italic text</i><a href="https://www.google.com">Click me!</a></div>')

    def test_to_html_multi_grandchildren_with_link(self):
        grandchild1 = LeafNode("b", "Bold text")
        grandchild2 = LeafNode(None, "Normal text")
        grandchild3 = LeafNode("i", "italic text")
        grandchild4 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        child1 = ParentNode("div", [grandchild1, grandchild2, grandchild3, grandchild4])
        child2 = LeafNode("p", "Hello, world!")
        child3 = ParentNode("div", [child1])
        parent_node = ParentNode("div", [child1, child2, child3])
        self.assertEqual(parent_node.to_html(),
        '<div><div><b>Bold text</b>Normal text<i>italic text</i><a href="https://www.google.com">Click me!</a></div><p>Hello, world!</p><div><div><b>Bold text</b>Normal text<i>italic text</i><a href="https://www.google.com">Click me!</a></div></div></div>')


# Errors
    def test_to_html_no_child(self):
        child_node = ParentNode("span", None)
        parent_node = ParentNode("div", [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_empty_children_list(self):
        child_node = ParentNode("span", [])
        parent_node = ParentNode("div", [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_empty_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode('', [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()