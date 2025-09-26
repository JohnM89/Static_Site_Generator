from enum import Enum   
from leafnode import LeafNode 
import re

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

# def extract_markdown_images(text):
#     alt_texts = re.findall(r"!\[[\w\s]+\]", text)
#     urls = re.findall(r"\([\S]+\)", text)
#     clean_alts = []
#     clean_urls = []
#     for alt in alt_texts:
#         clean_alts.append(alt.strip('![]')) 
#     for url in urls:
#         clean_urls.append(url.strip('()'))
#     extracted = list(zip(clean_alts, clean_urls))
#     return extracted

# def extract_markdown_links(text):
#     anchor_texts = re.findall(r"\[[\w\s]+\]", text)
#     urls = re.findall(r"\([\S]+\)", text)
#     clean_anchors = []
#     clean_urls = []
#     for anchor in anchor_texts:
#         clean_anchors.append(anchor.strip('[]')) 
#     for url in urls:
#         clean_urls.append(url.strip('()'))
#     extracted = list(zip(clean_anchors, clean_urls))
#     return extracted
#

#fixed - previous implementation didnt utilize regex grouping and was too brittle/greedy
def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

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

            
        
