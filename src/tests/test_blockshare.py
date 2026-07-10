import unittest
from src.leafnode import LeafNode
from src.blockshare import *

class TestBlockShare(unittest.TestCase):

    # Tests for markdown_to_blocks -------------------------------------------------------------------
    def test_markdown_to_blocks_one_blocks(self):
        md = """
                This is a paragraph with _italic_ text and `code` here   
                This is the same paragraph on a new line     
            """
        blocks = markdown_to_blocks(md)
        expected_blocks = [
                    "This is a paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line"
        ]
        self.assertListEqual(blocks, expected_blocks)

    def test_markdown_to_blocks_three_blocks(self):
        md = """
                This is **bolded** paragraph

                This is another paragraph with _italic_ text and `code` here
                This is the same paragraph on a new line

                - This is a list
                - with items
            """
        blocks = markdown_to_blocks(md)
        expected_blocks = [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
        ]
        self.assertListEqual(blocks, expected_blocks)

    # Tests for block_to_blocktype -------------------------------------------------------------------
    def test_block_to_blocktype_headings(self):
        markdown_h1 = "# This is a heading block"               # heading
        markdown_not_h1 = "#This is not a heading block"        # paragraph 
        markdown_h2 = "## this is h2 block"                     # heading
        markdown_h6 = "###### this is h6 block"                 # heading
        markdown_h7 = "####### there is no such thing as h7"    # paragraph
        markdown_not_heading = " # this is no heading"          # paragraph

        self.assertEqual(BlockType.HEADING, block_to_blocktype(markdown_h1))
        self.assertEqual(BlockType.HEADING, block_to_blocktype(markdown_h2))
        self.assertEqual(BlockType.HEADING, block_to_blocktype(markdown_h6))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(markdown_not_h1))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(markdown_h7))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(markdown_not_heading))

    def test_block_to_blocktype_code(self):
        # Expected BlockType.CODE
        code_1 = """```
                This is some code
                ```"""
        code_2 = "```\nThis is also some code```"

        # Expected BlockType.PARAGRAPH
        code_3 = "```This is not code```"
        code_4 = "```\nThis is also not code"
        code_5 = "This is not code```"

        self.assertEqual(BlockType.CODE, block_to_blocktype(code_1))
        self.assertEqual(BlockType.CODE, block_to_blocktype(code_2))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(code_3))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(code_5))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(code_4))

    def test_block_to_blocktype_quote(self):
        # Expected BlockType.QUOTE
        quote_1 = "> Quote 1"
        quote_2 = ">Quote 2"
        quote_3 = "> Quote 1\n> Quote 2\n> Quote 3"

        # Expected BlockType.PARAGRAPH
        quote_4 = " > Quote 4"
        quote_5 = "Quote 5"
        quote_6 = "> Quote 1\n > Quote 2\n > Quote 3"

        self.assertEqual(BlockType.QUOTE, block_to_blocktype(quote_1))
        self.assertEqual(BlockType.QUOTE, block_to_blocktype(quote_2))
        self.assertEqual(BlockType.QUOTE, block_to_blocktype(quote_3))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(quote_4))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(quote_5))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(quote_6))

    def test_block_to_blocktype_unordered_list(self):
        # Expected BlockType.UNORDERED_LIST
        list_1 = "- item 1"
        list_2 = "- item 1\n- item 2\n- item 3"

        # Expected BlockType.PARAGRAPH
        list_3 = "-item 1"
        list_4 = "- item 1\n-item2"
        list_5 = "- item 1\n- item2\n - item3"

        self.assertEqual(BlockType.UNORDERED_LIST, block_to_blocktype(list_1))
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_blocktype(list_2))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(list_3))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(list_4))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(list_5))

    def test_block_to_blocktype_ordered_list(self):
        # Expected BlockType.ORDERED_LIST
        list_1 = "1. item 1"
        list_2 = "1. item 1\n2. item 2\n3. item 3"

        # Expected BlockType.PARAGRAPH
        list_3 = "1 item 1"
        list_4 = "0. item 1"
        list_5 = "1.item 1"
        list_6 = "1. item 1\n2.item2"
        list_7 = "1. item 1\n2. item2\n3 . item3"
        list_8 = "1. item 1\n3. item2\n2. item3"

        self.assertEqual(BlockType.ORDERED_LIST, block_to_blocktype(list_1))
        self.assertEqual(BlockType.ORDERED_LIST, block_to_blocktype(list_2))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(list_3))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(list_4))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(list_5))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(list_6))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(list_7))
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(list_8))

    # TODO: Add tests for markdown_to_html_node, block_to_html_node
    # Tests for remove_markdown_from_block
    def test_remove_markdown_from_block_heading(self):

        block_heading_one = "# This is a heading"
        block_heading_two = "## This is a heading"
        block_heading_three = "### This is a heading"
        block_heading_four = "#### This is a heading"
        block_heading_five = "##### This is a heading"
        block_heading_six = "###### This is a heading"

        expected_result = "This is a heading"
        self.assertEqual(expected_result, remove_markdown_from_block(block_heading_one, BlockType.HEADING))
        self.assertEqual(expected_result, remove_markdown_from_block(block_heading_two, BlockType.HEADING))
        self.assertEqual(expected_result, remove_markdown_from_block(block_heading_three, BlockType.HEADING))
        self.assertEqual(expected_result, remove_markdown_from_block(block_heading_four, BlockType.HEADING))
        self.assertEqual(expected_result, remove_markdown_from_block(block_heading_five, BlockType.HEADING))
        self.assertEqual(expected_result, remove_markdown_from_block(block_heading_six, BlockType.HEADING))
    
    def test_remove_markdown_from_block_code(self):

        block_code = "```\nThis is a block of code```"
        expected_result = "This is a block of code"
        self.assertEqual(expected_result, remove_markdown_from_block(block_code, BlockType.CODE))
    
    def test_remove_markdown_from_block_quote(self):

        block_quote = """
            > This is quote 1
            > This is quote 2
            >This is quote 3
        """
        expected_result = "This is quote 1\nThis is quote 2\nThis is quote 3"
        self.assertEqual(expected_result, remove_markdown_from_block(block_quote, BlockType.QUOTE))
    
    def test_remove_markdown_from_block_unordered_list(self):

        block_unordered = """
            - This is item 1
            - This is item 2
            - This is item 3
        """
        expected_result = "This is item 1\nThis is item 2\nThis is item 3"
        self.assertEqual(expected_result, remove_markdown_from_block(block_unordered, BlockType.UNORDERED_LIST))
    
    def test_remove_markdown_from_block_ordered_list(self):

        block_ordered = """
            1. This is item 1
            2. This is item 2
            3. This is item 3
        """
        expected_result = "This is item 1\nThis is item 2\nThis is item 3"
        self.assertEqual(expected_result, remove_markdown_from_block(block_ordered, BlockType.ORDERED_LIST))

    # Tests for text_to_children
    def test_text_to_children_heading(self):

        block = "This is a **bold** and _italic_ heading"
        expected_children = [
            LeafNode(None, "This is a "),
            LeafNode("b", "bold"),
            LeafNode(None, " and "),
            LeafNode("i", "italic"),
            LeafNode(None, " heading"),
        ]
        expected_result = [
            ParentNode(None, expected_children) # type: ignore
        ]
        self.assertEqual(expected_result, text_to_children(block, BlockType.HEADING))

    def test_text_to_children_unordered_and_ordered_list(self):
        
        block = "This is **item** 1\nThis is _item_ 2\nThis is item 3"
        expected_quote_child_1 = [
            LeafNode(None, "This is "),
            LeafNode("b", "item"),
            LeafNode(None, " 1"),
        ]
        expected_quote_child_2 = [
            LeafNode(None, "This is "),
            LeafNode("i", "item"),
            LeafNode(None, " 2"),
        ]
        expected_quote_child_3 = [
            LeafNode(None, "This is item 3"),
        ]
        expected_result = [
            ParentNode("li", expected_quote_child_1), # type: ignore
            ParentNode("li", expected_quote_child_2), # type: ignore
            ParentNode("li", expected_quote_child_3), # type: ignore
        ]
        self.assertEqual(expected_result, text_to_children(block, BlockType.UNORDERED_LIST))
        self.assertEqual(expected_result, text_to_children(block, BlockType.ORDERED_LIST))

    def test_text_to_children_quote(self):
        
        block = "This is **quote** 1\nThis is _quote_ 2\nThis is quote 3"
        expected_quote_child_1 = [
            LeafNode(None, "This is "),
            LeafNode("b", "quote"),
            LeafNode(None, " 1"),
        ]
        expected_quote_child_2 = [
            LeafNode(None, "This is "),
            LeafNode("i", "quote"),
            LeafNode(None, " 2"),
        ]
        expected_quote_child_3 = [
            LeafNode(None, "This is quote 3"),
        ]
        expected_result = [
            ParentNode(None, expected_quote_child_1), # type: ignore
            ParentNode(None, expected_quote_child_2), # type: ignore
            ParentNode(None, expected_quote_child_3), # type: ignore
        ]
        self.assertEqual(expected_result, text_to_children(block, BlockType.QUOTE))

    def test_text_to_children_paragraph(self):
        
        block = "This is **line** 1\nThis is _line_ 2\nThis is line 3"
        expected_quote_child_1 = [
            LeafNode(None, "This is "),
            LeafNode("b", "line"),
            LeafNode(None, " 1"),
        ]
        expected_quote_child_2 = [
            LeafNode(None, "This is "),
            LeafNode("i", "line"),
            LeafNode(None, " 2"),
        ]
        expected_quote_child_3 = [
            LeafNode(None, "This is line 3"),
        ]
        expected_result = [
            ParentNode("p", expected_quote_child_1), # type: ignore
            ParentNode("p", expected_quote_child_2), # type: ignore
            ParentNode("p", expected_quote_child_3), # type: ignore
        ]
        self.assertEqual(expected_result, text_to_children(block, BlockType.PARAGRAPH))    

    # Tests for markdown_to_html_node
    # def test_paragraphs(self):
    #     md = """
    #         This is **bolded** paragraph
    #         text in a p
    #         tag here

    #         This is another paragraph with _italic_ text and `code` here

    #         """

    #     node = markdown_to_html_node(md)
    #     html = node.to_html()
    #     self.assertEqual(
    #         html,
    #         "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    #     )

    # def test_codeblock(self):
    #     md = """
    #         ```
    #             This is text that _should_ remain
    #             the **same** even with inline stuff
    #         ```
    #     """

    #     node = markdown_to_html_node(md)
    #     html = node.to_html()
    #     self.assertEqual(
    #         html,
    #         "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    #     )