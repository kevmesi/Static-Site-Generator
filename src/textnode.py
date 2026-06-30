from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():

    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        if not isinstance(other, TextNode):
            return NotImplemented
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.name}, {self.url})"
    
def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    
    match(text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return  LeafNode("code", text_node.text)
        case TextType.LINK:
            return  LeafNode("a", text_node.text, {"href": f"{text_node.url}"})
        case TextType.IMAGE:
            props = {
                "src": f"{text_node.url}",
                "alt" : f"{text_node.text}"
            }
            return LeafNode("img", "", props)

        case _: raise ValueError("unrecognized type")
    
