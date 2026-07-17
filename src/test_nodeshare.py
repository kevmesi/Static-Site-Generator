import unittest
from textnode import TextNode, TextType
from nodeshare import *

class testShare(unittest.TestCase):

    # Tests for split_nodes_delimiter -------------------------------------------------------------
    def test_split_nodes_delimiter_one_node_list_text_type_code(self):
        # print("Testing testShare.test_one_node_list_text_type_code... ")
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_two_node_list_text_type_bold(self):
        # print("Testing testShare.test_two_node_list_text_type_bold... ")
        node_1 = TextNode("This is text with a **bold block** word", TextType.TEXT)
        node_2 = TextNode("This is yet another text with a **also bold block** word.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node_1, node_2], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            TextNode("This is yet another text with a ", TextType.TEXT),
            TextNode("also bold block", TextType.BOLD),
            TextNode(" word.", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_one_node_list_no_matching_closing_delimiter(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        self.assertRaises(Exception, split_nodes_delimiter, [node], "`", TextType.CODE)

    def test_split_nodes_delimiter_one_node_list_two_delimiter_blocks(self):
        node = TextNode("This is text with a **first bold block** and a **second bold block** words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("first bold block", TextType.BOLD),
            TextNode(" and a ", TextType.TEXT),
            TextNode("second bold block", TextType.BOLD),
            TextNode(" words", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_one_node_list_three_delimiter_blocks(self):
        text = "This is text with a **first bold block** and a **second bold block** and last **third bold block** words"
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("first bold block", TextType.BOLD),
            TextNode(" and a ", TextType.TEXT),
            TextNode("second bold block", TextType.BOLD),
            TextNode(" and last ", TextType.TEXT),
            TextNode("third bold block", TextType.BOLD),
            TextNode(" words", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_one_node_list_two_delimiter_blocks_starts_and_ends_with_delimiter_block(self):
        node = TextNode("**First bold block** and a **second bold block** of words that are **important**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("First bold block", TextType.BOLD),
            TextNode(" and a ", TextType.TEXT),
            TextNode("second bold block", TextType.BOLD),
            TextNode(" of words that are ", TextType.TEXT),
            TextNode("important", TextType.BOLD),
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    # Tests for extract_markdown_images -----------------------------------------------------------
    def test_extract_markdown_images_no_images(self):
        text = "This is text with a no images and only one link [to boot dev](https://www.boot.dev)."
        matches = extract_markdown_images(text)
        expected_matches = []
        self.assertListEqual(matches, expected_matches)

    def test_extract_markdown_images_one_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)."
        matches = extract_markdown_images(text)
        expected_matches = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertListEqual(matches, expected_matches)

    def test_extract_markdown_images_two_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)."
        matches = extract_markdown_images(text)
        expected_matches = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(matches, expected_matches)

    # Tests for extract_markdown_links ----------------------------------------------------------------
    def test_extract_markdown_links_no_links(self):
        text = "This is text with a no links and only one image ![to boot dev](https://www.boot.dev)."
        matches = extract_markdown_links(text)
        expected_matches = []
        self.assertListEqual(matches, expected_matches)

    def test_extract_markdown_links_one_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        expected_matches = [
            ("to boot dev", "https://www.boot.dev")
        ]
        self.assertListEqual(matches, expected_matches)

    def test_extract_markdown_links_two_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected_matches = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(matches, expected_matches)

    # Tests for split_nodes_image ------------------------------------------------------------------------
    def test_split_nodes_image_no_images(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and text after the link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected_nodes = [
                TextNode("This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and text after the link", TextType.TEXT),
            ]
        self.assertListEqual(expected_nodes, new_nodes)

    def test_split_nodes_image_one_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and text after the image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected_nodes = [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and text after the image", TextType.TEXT),
            ]
        self.assertListEqual(expected_nodes, new_nodes)

    def test_split_nodes_image_one_image_starts_with_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) is a good image.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected_nodes = [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is a good image.", TextType.TEXT),
            ]
        self.assertListEqual(expected_nodes, new_nodes)

    def test_split_nodes_image_two_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected_nodes = [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ]
        self.assertListEqual(expected_nodes, new_nodes)

    def test_split_nodes_image_two_equal_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected_nodes = [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ]
        self.assertListEqual(expected_nodes, new_nodes)
    
    # Tests for split_nodes_link ------------------------------------------------------------------------
    def test_split_nodes_link_no_links(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and text after the image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected_nodes = [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and text after the image", TextType.TEXT),
            ]
        self.assertListEqual(expected_nodes, new_nodes)

    def test_split_nodes_link_one_link(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and text after the link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected_nodes = [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and text after the link", TextType.TEXT),
            ]
        self.assertListEqual(expected_nodes, new_nodes)

    def test_split_nodes_link_one_link_starts_with_link(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) is a good link.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected_nodes = [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is a good link.", TextType.TEXT),
            ]
        self.assertListEqual(expected_nodes, new_nodes)

    def test_split_nodes_link_two_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected_nodes = [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png")
            ]
        self.assertListEqual(expected_nodes, new_nodes)

    def test_split_nodes_link_two_equal_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected_nodes = [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            ]
        self.assertListEqual(expected_nodes, new_nodes)

    def test_split_nodes_link_same_image_and_link_before_the_link(self):
        node = TextNode(
            "This is text with an ![link](https://i.imgur.com/zjjcJKZ.png) and a [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected_nodes = [
                TextNode("This is text with an ![link](https://i.imgur.com/zjjcJKZ.png) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")
            ]
        self.assertListEqual(expected_nodes, new_nodes)

    # Tests for text_to_textnodes --------------------------------------------------------------------
    def test_text_to_textnodes_includes_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)."
        text_nodes = text_to_textnodes(text)
        expected_output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(text_nodes, expected_output)

    def test_text_to_textnodes_includes_none(self):
        text = "This is a smol text."
        text_nodes = text_to_textnodes(text)
        expected_output = [
            TextNode("This is a smol text.", TextType.TEXT),
        ]
        self.assertEqual(text_nodes, expected_output)