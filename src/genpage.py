from pathlib import Path    
from gencontent import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path, basepath):
        
        print(f"Generating page from {from_path} to {dest_path} using {template_path}")
        markdown = from_path.read_text()
        template = template_path.read_text()
        html_string = markdown_to_html_node(markdown).to_html()
        title = extract_title(markdown)
        out = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
        out = out.replace('href="/', f'href="{basepath}').replace('href="/', f'href="{basepath}')
        dest_path.parent.mkdir(parents=True,exist_ok=True)
        dest_path.write_text(out)

def generate_pages_recursive(from_path, template_path, dest_path, basepath): 
    for x in from_path.iterdir():
        if x.is_dir():
            generate_pages_recursive(x, template_path, dest_path / x.name, basepath)
        elif x.is_file() and x.name.endswith(".md"):
            generate_page(x, template_path, dest_path / "index.html", basepath)

        
        
        
        
        

