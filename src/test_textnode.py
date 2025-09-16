import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("this is a text node", TextType.LINK)
        node2 = TextNode("this is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def text_textnodenoteq(self):
        node = TextNode("this is a text node", TextType.LINK)
        node2 = TextNode("this is a text node", TextType.LINK) 
        self.assertIsNot(node, node2)

    def test_urlnotnone(self):
        node = TextNode("this is a text node", TextType.LINK, "http://something.com")
        self.assertIsNotNone(node)

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_url(self): 
        node = TextNode("this is a text node", TextType.LINK, "http://something.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props, {"href": "http://something.com"})
        self.assertEqual(html_node.value, "this is a text node")

    def test_bold(self):
        node = TextNode("this is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<b>this is a text node</b>')

    def test_img(self):
        node = TextNode("this is a text node", TextType.IMG, "../image")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<img src="../image" alt="this is a text node">')
if __name__ == "__main__":
    unittest.main()
