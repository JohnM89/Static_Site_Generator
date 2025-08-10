import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="h1", value="Blah", children=HTMLNode(tag="p", value="blah blah blah", props={"lang":"en-GB"}))
        node2 = HTMLNode(tag="h1", value="Blah", children=HTMLNode(tag="p", value="blah blah blah", props={"lang":"en-GB"}))
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = HTMLNode(tag="h1", value="Blah", children=HTMLNode(tag="p", value="blah blah blah", props={"lang":"en-GB"}))
        node2 = HTMLNode(tag="h2", value="Blah", children=HTMLNode(tag="p", value="blah2 blah2 blah2", props={"lang":"en-US"}))
        self.assertNotEqual(node, node2)

    def test_htmlnodenoteq(self):
        node = HTMLNode(tag="h1", value="Blah", children=HTMLNode(tag="p", value="blah blah blah", props={"lang":"en-GB"}))
        node2 = HTMLNode(tag="h2", value="Blah", children=HTMLNode(tag="p", value="blah blah blah", props={"lang":"en-GB"}))
        self.assertIsNot(node, node2)

    def test_tagnotnone(self):
        node = HTMLNode(tag="h1", value="Blah", children=HTMLNode(tag="p", value="blah blah blah", props={"lang":"en-GB"}))
        self.assertIsNotNone(node)

    def test_props_to_html_single_attr(self):
        node = HTMLNode(tag="h1", value="Blah", children=HTMLNode(tag="p", value="blah blah blah", props={"lang":"en-GB"}))
        expected = 'lang="en-GB" '
        self.assertEqual(node.children.props_to_html(), expected)
    
    def test_props_to_html_multi_attr(self):
        node = HTMLNode(props={"lang": "en-GB", "href": "https://boot.dev", "target": "_blank"})
        result = node.props_to_html()
        self.assertIn('href="https://boot.dev" ', result)
        self.assertIn('lang="en-GB" ', result)

    def test_props_method_is_none(self):
        node = HTMLNode()
        self.assertIsNone(node.props_to_html())

if __name__ == "__main__":
    unittest.main()
