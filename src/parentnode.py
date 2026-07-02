from src.htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str | None, children: list[HTMLNode] | None, props: dict[str, str] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("missing tag")
        
        if self.children is None or len(self.children) == 0:
            raise ValueError("missing children")
        
        html_format = f"<{self.tag}>"

        for child in self.children:
            html_format += child.to_html()

        html_format += f"</{self.tag}>"
        return html_format