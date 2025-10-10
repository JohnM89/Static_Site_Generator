from enum import Enum   
from leafnode import LeafNode
from parentnode import ParentNode
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

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

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
    markdown = markdown.lstrip("\n")
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


def block_to_block_type(text): 
    if re.match(r"#{1,6}\s+\S", text):
            return BlockType.HEADING
    if text.startswith("```") and text.endswith("```"):
            return BlockType.CODE
    lines = text.splitlines()
    if re.match(r">", lines[0]):
        #all returns true after checking .. all 
        if all(re.match(r">", line) for line in lines):
            return BlockType.QUOTE
    if re.match(r"- ", lines[0]):
        if all(re.match(r"- ", line) for line in lines):
            return BlockType.UNORDERED_LIST
    if re.match(r"1\.\s+", lines[0]):
        #enumerate yeilds a pair of (index, item) as we loop 
        if all(re.match(rf"{i}\.\s+", line) for i, line in enumerate(lines, 1)):
            return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nested_under_parent = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            if "\n" in block:
                text = " ".join(x.strip() for x in block.split("\n"))
                text = text.strip()
                child_nodes = text_to_textnodes(text) 
                parent = ParentNode(tag="p",children=[text_node_to_html_node(x) for x in child_nodes])
                nested_under_parent.append(parent)
                continue
            nested_under_parent.append(ParentNode(tag="p", children=[text_node_to_html_node(x) for x in text_to_textnodes(block.strip())]))
            continue
        if block_type == BlockType.HEADING:
            text = block.strip()
            count = 0
            for char in text:
                if char == "#":
                    count += 1
                else:
                    break
            if count + 1 >= len(text):
                raise ValueError(f"invalid heading level: {count}")
            text = text[count + 1 :]
            parent = ParentNode(tag=f"h{count}", children=[text_node_to_html_node(x) for x in text_to_textnodes(text.strip())])
            nested_under_parent.append(parent)
            continue
        if block_type == BlockType.CODE:
            #split by newlines and then dorp the starting backtics and ending ones 
            lines = block.split("\n")
            text = "\n".join(lines[1:-1])
            child = TextNode(text, TextType.PLAIN)
            parent = ParentNode(tag="code", children=text_node_to_html_node(child))
            nested_under_parent.append(ParentNode(tag="pre", children=parent))
            continue
        if block_type == BlockType.QUOTE:
            #instead of stripping or slicing we can sub the " > " with "" using re.sub 
            text = re.sub(r"^>\s?","", block)
            if "\n" in block:
                text = "\n".join(re.sub(r"^>\s?", "", x) for x in block.split("\n"))
                text = text.strip()
                child_nodes = text_to_textnodes(text)
                parent = ParentNode(tag="blockquote",children=[text_node_to_html_node(x) for x in child_nodes])
                nested_under_parent.append(parent)
                continue
            nested_under_parent.append(ParentNode(tag="blockquote", children=[text_node_to_html_node(x) for x in text_to_textnodes(text.strip())]))
            continue
        if block_type == BlockType.ORDERED_LIST:
            #likewise use re.sub for subbing out the ordered and unordered list chars
            text = re.sub(r"^\d+[.]\s", "", block)
            if "\n" in block:
                items = [re.sub(r"^\d+[.]\s", "", x) for x in block.split("\n")]
                child_nodes = []
                sub_children = []
                for item in items:
                    if item.strip():
                        children = text_to_textnodes(item)
                        sub_children.append(ParentNode(tag="li", children=[text_node_to_html_node(x) for x in children]))
                                
                parent = ParentNode(tag="ol", children=sub_children)
                nested_under_parent.append(parent)
                continue
            nested_under_parent.append(ParentNode(tag="ol",children=[ParentNode(tag="li",children=[text_node_to_html_node(x) for x in text_to_textnodes(text.strip())])]))
            continue
        if block_type == BlockType.UNORDERED_LIST:
            text = re.sub(r"^[-*+]\s", "", block)
            if "\n" in block:
                items = [re.sub(r"^[-*+]\s", "", x) for x in block.split("\n")]
                child_nodes = []
                sub_children = []
                for item in items:
                    if item.strip():

                        children = text_to_textnodes(item)
                        sub_children.append(ParentNode(tag="li", children=[text_node_to_html_node(x) for x in children]))
                                
                parent = ParentNode(tag="ul", children=sub_children)
                nested_under_parent.append(parent)
                continue
            nested_under_parent.append(ParentNode(tag="ul",children=[ParentNode(tag="li",children=[text_node_to_html_node(x) for x in text_to_textnodes(text.strip())])]))
            continue
            
    return ParentNode(tag="div", children=nested_under_parent)
