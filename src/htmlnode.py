class HTMLNode():
    def __init__(self, tag: str | None = None, value: str | None = None, children: list[HTMLNode] | None = None, props: dict[str, str] | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplemented
    
    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        
        formatted_string = ""
        for prop in self.props:
            formatted_string += " " + f"{prop}=\"{self.props[prop]}\""

        return formatted_string 
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    


