from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

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
    Multiline Code blocks must start with 3 backticks and a newline, then end with 3 backticks.
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