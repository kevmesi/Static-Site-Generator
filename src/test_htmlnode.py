import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_no_props(self):
        testHTMLNode = HTMLNode(None, None, None, None)

        expected_outcome = ""
        real_outcome = testHTMLNode.props_to_html()
        self.assertEqual(expected_outcome, real_outcome)

    def test_props_to_html_one_prop(self):
        testProps = dict()
        testProps["href"] = "https://www.google.com"

        testHTMLNode = HTMLNode(None, None, None, testProps)

        expected_outcome = ' href="https://www.google.com"'
        real_outcome = testHTMLNode.props_to_html()
        self.assertEqual(expected_outcome, real_outcome)

    def test_props_to_html_two_props(self):
        testProps = dict()
        testProps["href"] = "https://www.google.com"
        testProps["target"] ="_blank"

        testHTMLNode = HTMLNode(None, None, None, testProps)

        expected_outcome = ' href="https://www.google.com" target="_blank"'
        real_outcome = testHTMLNode.props_to_html()
        self.assertEqual(expected_outcome, real_outcome)
