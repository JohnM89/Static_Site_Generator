import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html(self):
        #test multiple tags
        tags = ["p", "div", "span", "h1"]
        for tag in tags:
            with self.subTest(tag=tag):
                node = LeafNode(tag=tag, value="Blah", props={"lang":"en-GB"})
                self.assertEqual(node.to_html(), f'<{tag} lang="en-GB">"Blah"</{tag}>')

    def test_no_tag(self):
        node = LeafNode(value="Blah", props={"lang":"en-GB"})
        self.assertEqual(node.to_html(), "Blah")

    def test_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode(tag="h2", props={"lang":"en-GB"})
            node.to_html()
    

if __name__ == "__main__":
    unittest.main()
