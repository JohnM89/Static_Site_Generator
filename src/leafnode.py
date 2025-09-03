from htmlnode import HTMLNode   


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)


    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"    
    
    def to_html(self):
        
        if self.value is None:
            raise ValueError("Value can't be NoneType")
        if self.tag is None:
            return self.value
 
        return f'<{self.tag}{self.props_to_html() if self.props else ""}>"{self.value}"</{self.tag}>'

            
