import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_href(self):
        node = HTMLNode('a', 'Click me', None, {'href': 'https://example.com'})
        self.assertEqual(node.props_to_html(), 'href=https://example.com')
    def test_props_to_html_with_no_props(self):
        node = HTMLNode('a', 'Click me', None, )
        self.assertEqual(node.props_to_html(), '')
    def test_props_to_html_with_multiple(self):
        node = HTMLNode('a', 'Click me', None, {'href': 'https://example.com', 'target': '_blank'})
        self.assertEqual(node.props_to_html(), 'href=https://example.com target=_blank')
    def test_repr(self):
        node = HTMLNode('a', 'Click me', None, {'href': 'https://example.com', 'target': '_blank'})
        expected = "HTMLNode(a, Click me, None, {'href': 'https://example.com', 'target': '_blank'})"
        self.assertEqual(node.__repr__(), expected)

if __name__ == "__main__":
    unittest.main()