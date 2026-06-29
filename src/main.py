from textnode import TextNode, TextType

def main() -> None:
    
    dummy_text = "This is some anchor text"
    dummy_text_type = TextType.ITALIC
    dummy_url = "https://www.boot.dev"
    dummy_node = TextNode(dummy_text, dummy_text_type, dummy_url)
    print(dummy_node)


main()