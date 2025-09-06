import unittest
import random
from parentnode import ParentNode
from leafnode import LeafNode   
#from htmlnode import HTMLNode


class TestParentNode(unittest.TestCase):
    #
    def test_grandchild_to_html(self):
        #test multiple tags
        tags = ["div", "p", "span", "h1"]
        grandchildren = [LeafNode("p", "Blah"), LeafNode("div", "Blah"), LeafNode("span", "Blah")]
        children = []
        tagcount = 0
        for gchild in grandchildren:
            children.append(ParentNode(tags[tagcount], [gchild]))
            tagcount += 1
        for child in children:
            with self.subTest(child=child):
                node = ParentNode("div", [child], props={"lang":"en-GB"})
                node2 = ParentNode("div", [child], props={"lang":"en-GB"})

                self.assertEqual(node.to_html(), node2.to_html())

    def test_nested_child_and_grandchild_to_html(self):
       
        rnd = random.Random(42)
        tags = ["div", "p", "span", "h1"]
        grandchildren = [LeafNode("p", "Blah"), LeafNode("div", "Blah"), LeafNode("span", "Blah")]
        grandchildrenparent = [ParentNode("p", [grandchildren[rnd.randint(0, 2)]]), ParentNode("div", [grandchildren[rnd.randint(0, 2)]]), ParentNode("span", [grandchildren[rnd.randint(0, 2)]])]
        children = []
        tagcount = 0
        for gchild in grandchildren:
            nested = rnd.randint(0, 1)
            if nested == 1:
                pick = rnd.choice(grandchildrenparent)
                children.append(ParentNode(tags[tagcount], [gchild, pick]))
            else:
                children.append(ParentNode(tags[tagcount], [gchild]))
            tagcount += 1
        for child in children:
            with self.subTest(child=child):
                node = ParentNode("div", [child], props={"lang":"en-GB"})
                node2 = ParentNode("div", [child], props={"lang":"en-GB"})

                self.assertEqual(node.to_html(), node2.to_html())


    def test_child_to_html(self):
        children = [LeafNode("p", "Blah"), LeafNode("div", "Blah"), LeafNode("span", "Blah")]
        for child in children:
            with self.subTest(child=child):
                node = ParentNode("div", [child])
                self.assertEqual(node.to_html(), f'<div>{child.to_html()}</div>')

    def test_equal(self):
        node = ParentNode(tag="div", children=[LeafNode("p", "Blah")], props={"lang":"en-GB"})
        node2 = ParentNode(tag="div", children=[LeafNode("p", "Blah")], props={"lang":"en-GB"})
        self.assertEqual(node.to_html(), node2.to_html())
    #
    def test_no_value(self):

        with self.assertRaises(ValueError):

            node = ParentNode("h2", None, props={"lang":"en-GB"})
            node.to_html()

    def test_missing_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, [LeafNode(None, "x")])
            node.to_html()


if __name__ == "__main__":
    unittest.main()
