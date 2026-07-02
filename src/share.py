import re
from src.textnode import TextNode, TextType

def text_to_textnodes(text: str) -> list[TextNode]:
    """
    Converts text to a list of textnodes.\n
    Uses:\n
        split_nodes_delimiter to extract TextTypes: BOLD, ITALIC and CODE,\n
        split_nodes_image to extract TextType IMAGE,\n
        split_nodes_link to extract TextType LINK.
    """
    first_node = TextNode(text, TextType.TEXT)
    extract_bold = split_nodes_delimiter([first_node], "**", TextType.BOLD)
    extract_italic = split_nodes_delimiter(extract_bold, "_", TextType.ITALIC)
    extract_code = split_nodes_delimiter(extract_italic, "`", TextType.CODE)
    extract_images = split_nodes_image(extract_code)
    extract_links = split_nodes_link(extract_images)
    return extract_links


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """
    Return a new list of nodes, where any "text" type nodes in the input list are (potentially) split into multiple nodes based on the syntax.\n
    Used only for TextTypes: BOLD, ITALIC and CODE (e.g. ** for bold, _ for italic, and a backtick ` for code)
    """
    split_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)
        delimiter_count = node.text.count(delimiter)

        if delimiter_count % 2 != 0 : # matching closing delimiter is not found
            raise Exception("invalid Markdown sintax... matching closing delimiter not found")

        for index in range(len(split_text)):
            text = split_text[index]
            if len(text) == 0: # happens when the delimiter is in the beginning or the end of the text
                continue

            if index % 2 == 1: # text between the delimiters
                text_node = TextNode(text, text_type)
            else:
                text_node = TextNode(text, TextType.TEXT)

            split_nodes.append(text_node)

    return split_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Return a new list of nodes, where any "text" type nodes in the input list are (potentially) split into multiple nodes among which are **image** nodes.
    """
    split_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
            continue

        text = node.text
        extracted_images = extract_markdown_images(text)

        for image in extracted_images:
            alt_text, image_url = image[0],  image[1]
            image_markdown = f"![{alt_text}]({image_url})"

            # Add the node for text before the image and the node for the image
            index = text.find(image_markdown)
            node_text = text[:index]
            if len(node_text) > 0:
                new_node = TextNode(node_text, TextType.TEXT)
                split_nodes.append(new_node)

            image_node = TextNode(alt_text, TextType.IMAGE, image_url)
            split_nodes.append(image_node)

            # Crop text to after the image
            text = text[index + len(image_markdown):]

        # Add the part of text after the last image (if there is any)
        if len(text) > 0:
            new_node = TextNode(text, TextType.TEXT)
            split_nodes.append(new_node)

    return split_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Return a new list of nodes, where any "text" type nodes in the input list are (potentially) split into multiple nodes among which are **link** nodes.
    """
    split_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
            continue

        text = node.text
        extracted_links = extract_markdown_links(text)

        for link in extracted_links:
            anchor_text, link_url = link[0],  link[1]
            link_markdown = f"[{anchor_text}]({link_url})"

            link_index = text.find(link_markdown)

            # Case when there is an image and link with same 
            possible_image_markdown = f"![{anchor_text}]({link_url})"
            possible_image_index = text.find(possible_image_markdown)
            while 0 < possible_image_index < link_index:
                # Found the exception - skip it
                link_index = text.find(link_markdown, link_index + 1)
                possible_image_index = text.find(possible_image_markdown, possible_image_index + 1)

            # Add the node for text before the link and the node for the link
            node_text = text[:link_index]
            if len(node_text) > 0:
                new_node = TextNode(node_text, TextType.TEXT)
                split_nodes.append(new_node)

            link_node = TextNode(anchor_text, TextType.LINK, link_url)
            split_nodes.append(link_node)

            # Crop text to after the link
            text = text[link_index + len(link_markdown):]

        # Add the part of text after the last link (if there is any)
        if len(text) > 0:
            new_node = TextNode(text, TextType.TEXT)
            split_nodes.append(new_node)

    return split_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """
    Takes raw markdown text and returns a list of tuples.\n
    Each tuple should contain the alt text and the URL of any markdown images.
    """ 
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """
    Takes raw markdown text and returns a list of tuples.\n
    Each tuple should contain the anchor text and the URL of any markdown links.
    """ 
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)