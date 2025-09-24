from enum import Enum   
from leafnode import LeafNode 

class DelimiterType(Enum):
    BOLD = "**"
    ITALIC = "_"
    CODE = "`"

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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    delim = delimiter.value if isinstance(delimiter, DelimiterType) else delimiter
    allowed_delimiter_types = {'**', '`', '_'}
    if not isinstance(delim, str) or delim not in allowed_delimiter_types:
        raise ValueError("Not a valid delimiter type")
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        elif delim not in node.text:
            new_nodes.append(node)
            continue
        else:
            split_nodes = node.text.split(delim, maxsplit=2)
            if len(split_nodes) == 2:
                raise ValueError("Unmatched delimiter")
            node_a, node_b, node_c = split_nodes
            if node_a:
                new_nodes.append(TextNode(node_a, TextType.PLAIN))
            new_nodes.append(TextNode(node_b, text_type))
            if len(node_c) != 0:
                new_nodes.extend(split_nodes_delimiter([TextNode(node_c, TextType.PLAIN)], delimiter, text_type))
    return new_nodes
        

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

            
        
