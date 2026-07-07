from enum import Enum
import re
from src.htmlnode import HTMLNode
from src.nodeshare import text_to_textnodes
from src.parentnode import ParentNode
from src.textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_html_node(markdown: str) -> HTMLNode:

    markdown_blocks = markdown_to_blocks(markdown)
    children = []

    for block in markdown_blocks:

        block_type = block_to_blocktype(block)
        html_node = block_to_html_node(block, block_type)
        children.append(html_node)

    return ParentNode("div", children)

def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Takes a raw Markdown string (representing a full document) as input and returns a list of "block" strings.
    """
    lines = markdown.split("\n\n")
    markdown_blocks = []
    for line in lines:
        if len(line) > 0:
            line = remove_identation_tabs_from_paragraph(line)
            markdown_blocks.append(line)

    return markdown_blocks

def block_to_html_node(block: str, block_type: BlockType) -> HTMLNode:

    filtered_block = remove_markdown_from_block(block, block_type)

    match(block_type):
        case BlockType.HEADING:
            heading_type = block.count("#", 0, block.find(" "))
            html_tag = "h" + str(heading_type)
        case BlockType.CODE:
            html_tag = "pre"      
        case BlockType.QUOTE:
            html_tag = "blockquote"
        case BlockType.UNORDERED_LIST:
            html_tag = "ul"
        case BlockType.ORDERED_LIST:
            html_tag = "ol"
        case _: 
            html_tag = "p"

    if block_type == BlockType.CODE: # Special case for BlockType.CODE - we dont want to handle inline markup
        htmlnode = ParentNode(html_tag, [text_node_to_html_node(TextNode(block, TextType.CODE))])
    else:
        htmlnode = ParentNode(html_tag, text_to_children(filtered_block, block_type))

    return htmlnode

def text_to_children(block: str, block_type: BlockType) -> list[HTMLNode]:

    block_children_html = []
    html_tag = None

    # Define html_tag and handle special case of BlockType.CODE
    match(block_type):
        case BlockType.HEADING:
            html_tag = None
        case BlockType.CODE: # Special case in which we do not transform inline markup
            return []
        case BlockType.QUOTE:
            html_tag = None
        case BlockType.UNORDERED_LIST:
            html_tag = "li"
        case BlockType.ORDERED_LIST:
            html_tag = "li"
        case _: 
            html_tag = "p"

    # Transform each line in block into children as HTMLNodes
    block_lines = block.splitlines()
            
    for line in block_lines:

        line_children_htmlnodes = []
        line_children_textnodes = text_to_textnodes(line)
                
        for child in line_children_textnodes:
            line_children_htmlnodes.append(text_node_to_html_node(child))

        block_children_html.append(ParentNode(html_tag, line_children_htmlnodes))
    
    return block_children_html

def remove_markdown_from_block(block: str, block_type: BlockType) -> str:

    match(block_type):
        case BlockType.HEADING:
            heading_type = block.count("#", 0, block.find(" "))
            prefix = "#" * heading_type + " "
            return block.removeprefix(prefix)
            
        case BlockType.CODE:
            return block.removeprefix("```\n").removesuffix("```")

        case BlockType.QUOTE:
            block_lines = block.splitlines()
            for line in block_lines:
                line = line.removeprefix("> ").removeprefix(">")
            return "\n".join(block_lines)
            
        case BlockType.UNORDERED_LIST:
            block_lines = block.splitlines()
            for line in block_lines:
                line = line.removeprefix("- ")
            return "\n".join(block_lines)

        case BlockType.ORDERED_LIST:
            block_lines = block.splitlines()
            index = 0
            for line in block_lines:
                prefix = str(index) + ". "
                line = line.removeprefix(prefix)
                index += 1
            return "\n".join(block_lines)
        
        case _:
            return block

def block_to_blocktype(markdown_block: str) -> BlockType:
    """
    Takes a single block of markdown text as input and returns the BlockType representing the type of block it is.
    """
    if is_block_heading(markdown_block):
        return BlockType.HEADING
    
    if is_block_code(markdown_block):
        return BlockType.CODE
    
    if is_block_quote(markdown_block):
        return BlockType.QUOTE
    
    if is_block_unordered_list(markdown_block):
        return BlockType.UNORDERED_LIST
    
    if is_block_ordered_list(markdown_block):
        return BlockType.ORDERED_LIST
    
    # If none of the above conditions are met, the block is a normal paragraph.
    return BlockType.PARAGRAPH

def is_block_heading(markdown_block: str) -> bool:
    """
    Headings start with 1-6 # characters, followed by a space and then the heading text.
    """
    return re.search(r"^#{1,6} \w+", markdown_block, re.MULTILINE) is not None

def is_block_code(markdown_block: str) -> bool:
    """
    Multiline code blocks must start with 3 backticks and a newline, then end with 3 backticks.
    """
    return markdown_block.startswith("```\n") and markdown_block.endswith("```")

def is_block_quote(markdown_block: str) -> bool:
    """
    Every line in a quote block must start with a "greater-than" character: > followed by the quote text.\n
    A space after > is allowed but not required.
    """
    block_lines = markdown_block.splitlines()
    for line in block_lines:
        if not line.startswith(">"):
            return False   
    return True

def is_block_unordered_list(markdown_block: str) -> bool:
    """
    Every line in an unordered list block must start with a - character, followed by a space.
    """
    block_lines = markdown_block.splitlines()
    for line in block_lines:
        if not line.startswith("- "):
            return False   
    return True

def is_block_ordered_list(markdown_block: str) -> bool:
    """
    Every line in an ordered list block must start with a number followed by a . character and a space.\n
    The number must start at 1 and increment by 1 for each line.
    """
    block_lines = markdown_block.splitlines()
    for index in range(1, len(block_lines) + 1):
        line = block_lines[index - 1]
        if not line.startswith(f"{index}. "):
            return False
        
    return True

def remove_identation_tabs_from_paragraph(paragraph: str) -> str:

    lines = paragraph.split("\n")

    if len(lines) == 1:
        # Nothing to remove - pargraph only had one line
        return paragraph

    clean_paragraph = ""
    for line in lines:
        clean_paragraph += line.strip() + "\n"

    clean_paragraph = clean_paragraph.strip("\n")
    return clean_paragraph