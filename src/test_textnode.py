import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):

    # Tests for text_node_to_html_node ---------------------------
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://url.org")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href" : "https://url.org"})

    def test_image(self):
        node = TextNode("This is alt text for image node", TextType.IMAGE, "https://url.org")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src" : "https://url.org", "alt" : "This is alt text for image node"})
 
    # Test for equality ------------------------------------------
    def test_eq_no_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://url.org")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://url.org")
        self.assertEqual(node, node2)

    def test_not_eq_no_url_diff_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a second text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_no_url_diff_text_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_one_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://url.org")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    # -------------------------------------------------------------
