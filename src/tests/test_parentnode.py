import unittest
from src.parentnode import ParentNode
from src.leafnode import LeafNode

class TestParentNode(unittest.TestCase):

    # Test for no tag
    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        self.assertRaises(ValueError, parent_node.to_html)

    # Tests for children and grandchildren -------------------
    def test_to_html_with_no_children_none(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_no_children_empty_list(self):
        parent_node = ParentNode("div", [])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_one_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_two_children(self):
        child_node1 = LeafNode("span", "child")
        child_node2 = LeafNode("b", "bold child")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><b>bold child</b></div>")

    def test_to_html_with_no_grandchildren_none(self):
        child_node = ParentNode("span", None)
        parent_node = ParentNode("div", [child_node])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_no_grandchildren_empty_list(self):
        child_node = ParentNode("span", [])
        parent_node = ParentNode("div", [child_node])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_one_grandchild(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_two_grandchildren(self):
        grandchild_node1 = LeafNode("b", "bold grandchild")
        grandchild_node2 = LeafNode("i", "italic grandchild")
        child_node = ParentNode("span", [grandchild_node1, grandchild_node2])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>bold grandchild</b><i>italic grandchild</i></span></div>",
        )
    
    def test_to_html_with_two_children_and_three_grandchildren(self):
        grandchild_node1 = LeafNode("b", "bold grandchild")
        grandchild_node2 = LeafNode("i", "italic grandchild")
        child_node1 = ParentNode("span", [grandchild_node1, grandchild_node2])
        grandchild_node3 = LeafNode("p", "paragraph grandchild")
        child_node2 = ParentNode("div", [grandchild_node3])
        
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>bold grandchild</b><i>italic grandchild</i></span><div><p>paragraph grandchild</p></div></div>",
        )
    # -----------------------------------------------------------