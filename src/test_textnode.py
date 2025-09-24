import unittest

from textnode import TextNode, TextType, DelimiterType, text_node_to_html_node, split_nodes_delimiter


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

class TestInlineMarkdown(unittest.TestCase):
    def test_delimiter(self):

        delimiters = [DelimiterType.BOLD, DelimiterType.CODE, DelimiterType.ITALIC]
        test_types = [TextType.BOLD, TextType.CODE, TextType.ITALIC]
        test_delim = ["**bolded phrase**","`code`","_italic phrase_"]
        post_strip = ['bolded phrase', 'code', 'italic phrase']
        i = 0
        
        old_nodes = [TextNode(f"This is text with a {test_delim[0]} in the middle", TextType.PLAIN), TextNode(f"This is text with a {test_delim[1]} in the middle", TextType.PLAIN), TextNode(f"This is text with a {test_delim[2]} in the middle", TextType.PLAIN)]

        for delimiter in delimiters:
            new_nodes = split_nodes_delimiter(old_nodes, delimiter, test_types[i])

            self.assertEqual(new_nodes[1 + i], TextNode(post_strip[i],test_types[i]))
            i += 1

    def test_delim_bold(self):
        node = TextNode("this is a text with **bolded words** and some more **bolded words**", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], DelimiterType.BOLD, TextType.BOLD)
        self.assertListEqual([
            TextNode("this is a text with ", TextType.PLAIN),
            TextNode("bolded words", TextType.BOLD),
            TextNode(" and some more ", TextType.PLAIN),
            TextNode("bolded words", TextType.BOLD)
        ], new_nodes)

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], DelimiterType.BOLD, TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, DelimiterType.ITALIC, TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )
if __name__ == "__main__":
    unittest.main()
