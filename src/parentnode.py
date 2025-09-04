from htmlnode import HTMLNode   

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        self.tag = tag
        if not isinstance(children, list) and children is not None:
            self.children = [children]
        else:
            self.children = children
        self.props = props  

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag can't be None")
        if self.children is None:
            raise ValueError("children can't be None")
        children_html = ""
        if self.children is not None:
            for child in self.children:
                children_html += child.to_html()
            return f'<{self.tag}{self.props_to_html() if self.props else ""}>{children_html}</{self.tag}>'



    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
            
