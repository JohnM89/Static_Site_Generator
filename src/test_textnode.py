import unittest
from textnode import TextNode, TextType, DelimiterType, BlockType, markdown_to_html_node, block_to_block_type, markdown_to_blocks, text_to_textnodes, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link



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
    def test_markdown_images(self):
        text = "This is text with a ![rick roll oi](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted = extract_markdown_images(text)
        self.assertEqual(extracted, ('rick roll oi', 'https://i.imgur.com/aKaOqIh.gif'))

    def test_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"        
        extracted = extract_markdown_links(text)
        self.assertEqual(extracted , ('to boot dev', 'https://www.boot.dev'))

    def test_image_markdown_to_nodes(self):
        node = TextNode(
        "This is text with a image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        
        self.assertListEqual(new_nodes,
        [
            TextNode("This is text with a image ", TextType.PLAIN),
            TextNode("to boot dev", TextType.IMG, "https://www.boot.dev"),
            TextNode(" and ", TextType.PLAIN),
            TextNode(
                "to youtube", TextType.IMG, "https://www.youtube.com/@bootdotdev"
            ),
        ])
    def test_link_markdown_to_nodes(self):
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        
        self.assertListEqual(new_nodes,
        [
            TextNode("This is text with a link ", TextType.PLAIN),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.PLAIN),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ])
    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(new_nodes, 
        [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMG, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])
    #make sure test functions start with "test_" or they wont be discovered
    def test_block_to_block_type_test(self):
        text = ">This is a quote"
        type_of = block_to_block_type(text)
        self.assertEqual(BlockType.QUOTE, type_of)
    
    def test_block_to_block_type_test_two(self):
        #no spaces allowed between newlines that would be a user formatting issue
        texts = ["## header\n#### header", ">This is a quote\n>this is a quote too", "This is a regular paragraph", "```this is\ncode```", "- this is a ul\n- so is this", "1. this\n2. is\n3. some ol", "3. this is regular paragraph"]
        asserts = [BlockType.HEADING, BlockType.QUOTE, BlockType.PARAGRAPH, BlockType.CODE, BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST, BlockType.PARAGRAPH]
        inx = 0
        for text in texts:
            type_of = block_to_block_type(text)
            self.assertEqual(asserts[inx], type_of)
            inx += 1

    def test_markdown_to_html_node_paragraph(self):
        md = """
This is **bolded** paragraph text in a p tag
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is <b>bolded</b> paragraph text in a p tag</p></div>")
    
    def test_markdown_to_html_node_heading(self):
        md = """
## This is **bolded** header text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2>This is <b>bolded</b> header text</h2></div>")
    def test_markdown_to_html_node_quote(self):
        md = """
> Famous Quote:
> He who fizz must also
> bizz
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>Famous Quote:\nHe who fizz must also\nbizz</blockquote></div>")
    def test_markdown_to_html_node_ordered_list(self):
        md = """
1. hat
2. shoes
3. something
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>hat</li><li>shoes</li><li>something</li></ol></div>")
    def test_markdown_to_html_node_code(self):
        md = """```
- hat
- shoes
- something
```"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><pre><code>- hat\n- shoes\n- something</code></pre></div>")
    def test_markdown_to_html_node_unordered_list(self):
        md = """
- hat
- shoes
- something
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>hat</li><li>shoes</li><li>something</li></ul></div>")
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(blocks,
        [
        "This is **bolded** paragraph",
        "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
        "- This is a list\n- with items",
        ],
        )

    def test_markdown_to_again(self):
        md = """This is **bolded** paragraph

This is another paragraph with **bold** text and _italics_ here
This is the same paragraph on a new line



- This is a list

- with items"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(blocks,
        [
        "This is **bolded** paragraph",
        "This is another paragraph with **bold** text and _italics_ here\nThis is the same paragraph on a new line",
        "- This is a list",
        "- with items",
        ],
        )


if __name__ == "__main__":
    unittest.main()
