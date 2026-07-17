import unittest
from leafnode import LeafNode
from htmlnode import HTMLNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected_outcome = '<a href="https://www.google.com">Click me!</a>'
        real_outcome = node.to_html()
        self.assertEqual(expected_outcome, real_outcome)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "No tags!")
        self.assertEqual(node.to_html(), "No tags!")

    def test_leaf_to_html_no_value(self):
        node = LeafNode(None, "")
        node.value = None # making sure that the value is None since it cannot be none in init
        self.assertRaises(ValueError, node.to_html)
