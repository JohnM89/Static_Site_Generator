import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()
