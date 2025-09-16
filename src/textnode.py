from enum import Enum   
from leafnode import LeafNode 

class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMG = "img"  

class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, obj):
        if isinstance(obj, TextNode):
            return self.text == obj.text and self.text_type == obj.text_type and self.url == obj.url
        return False

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'
    
def text_node_to_html_node(textnode):
    tag = None
    prop = None
    value = textnode.text
    if not isinstance(textnode.text_type, TextType):
        raise ValueError(f"not a valid type: {textnode.text_type}")
    
    if textnode.text_type == TextType.BOLD:
        tag = "b"
    if textnode.text_type == TextType.ITALIC:
        tag = "i"
    if textnode.text_type == TextType.CODE:
        tag = "code"
    if textnode.text_type == TextType.LINK:
        tag = "a"
        prop = {"href": textnode.url}
    if textnode.text_type == TextType.IMG:
        tag = "img"
        value = ""
        prop = {"src": textnode.url, "alt": textnode.text}
    return LeafNode(tag=tag, value=value, props=prop)

            
        
