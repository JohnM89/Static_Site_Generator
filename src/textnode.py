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

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.search(pattern, text)
    if matches:
        return matches.groups()
    return None


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.search(pattern, text)
    if matches:
        return matches.groups()
    return None

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        image_markdown = extract_markdown_images(node.text)
        
        if image_markdown:
            delim = f"![{image_markdown[0]}]({image_markdown[1]})"
            if delim not in node.text:
                new_nodes.append(node)
                continue
            split_nodes = node.text.split(delim , maxsplit=1)

            if len(split_nodes) != 2:
                raise ValueError("invalid markdown, image section not closed")
            node_a, node_b = split_nodes

            if node_a:
                new_nodes.append(TextNode(node_a, TextType.PLAIN))

            new_nodes.append(TextNode(image_markdown[0], TextType.IMG, image_markdown[1]))
            if len(node_b) != 0:
                new_nodes.extend(split_nodes_image([TextNode(node_b, TextType.PLAIN)]))
        else:
            new_nodes.append(node)

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        link_markdown = extract_markdown_links(node.text)
        if link_markdown:

            delim = f"[{link_markdown[0]}]({link_markdown[1]})"
            if delim not in node.text:
                new_nodes.append(node)
                continue
            split_nodes = node.text.split(delim , maxsplit=1)
            if len(split_nodes) != 2:
                raise ValueError("invalid markdown, link section not closed")
            node_a, node_b = split_nodes

            if node_a:
                new_nodes.append(TextNode(node_a, TextType.PLAIN))

            new_nodes.append(TextNode(link_markdown[0], TextType.LINK, link_markdown[1]))
            if len(node_b) != 0:
                new_nodes.extend(split_nodes_link([TextNode(node_b, TextType.PLAIN)]))
        else:
            new_nodes.append(node)

    return new_nodes

def text_to_textnodes(text):
    new_node = [TextNode(text, TextType.PLAIN)]
    allowed_delimiter_types = [('**', TextType.BOLD), ('`', TextType.CODE), ('_', TextType.ITALIC),]
    for type_of in allowed_delimiter_types:
        new_node = split_nodes_delimiter(new_node, type_of[0], type_of[1])
    new_node = split_nodes_link(new_node)
    new_node = split_nodes_image(new_node)
    return new_node

def markdown_to_blocks(markdown):
    block_strings = markdown.split("\n\n")
    clean = []
    for block in block_strings:
        block.strip()
        if not block:
            continue
        clean.append(block)
    return clean


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

            
        
