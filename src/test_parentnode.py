import unittest

from parentnode import ParentNode
from leafnode import LeafNode   
#from htmlnode import HTMLNode


class TestParentNode(unittest.TestCase):
    #
    def test_leaf_to_html(self):
        #test multiple tags
        tags = ["div", "p", "span", "h1"]
        grandchildren = [LeafNode("p", "Blah"), LeafNode("div", "Blah"), LeafNode("span", "Blah")]
        children = []
        tagcount = 0
        for gchild in grandchildren:
            children.append(ParentNode(tags[tagcount], [gchild]))
            tagcount += 1
        for child in children:
            with self.subTest(children=child):
                node = ParentNode("div", children, props={"lang":"en-GB"})
                self.assertEqual(node.to_html(), f'<div lang="en-GB">"Blah"</div>')

    def test_equal(self):
        node = ParentNode(tag="div", children=LeafNode("p", "Blah"), props={"lang":"en-GB"})
        node2 = ParentNode(tag="div", children=LeafNode("p", "Blah"), props={"lang":"en-GB"})
        self.assertEqual(node.to_html(), node2.to_html())
    #
    def test_no_value(self):

        with self.assertRaises(ValueError):

            node = ParentNode("h2", None, props={"lang":"en-GB"})
            node.to_html()



if __name__ == "__main__":
    unittest.main()
