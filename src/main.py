from textnode import TextNode, TextType      
import shutil
from pathlib import Path
from copystatic import copy_to_public
def main():
    new_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
        
    def clean_up_public_and_copy():
        cwd = Path.cwd()
        #set walk back /src/main.py to ../
        project_root = cwd

        #Path object overloads the "/" operator to join paths cleanly
        path_static = project_root / "static"
        path_public = project_root / "public"
        if not path_static.exists():
            raise FileNotFoundError(f"missing source: {path_static}")
        if not path_static.is_dir():
            raise NotADirectoryError(f"source is not a directory: {path_static}")
        
        if path_public.exists() and path_public.is_dir():
            shutil.rmtree(path_public)
        path_public.mkdir()
        copy_to_public(path_static, path_public)
        
    clean_up_public_and_copy()

if __name__ == "__main__":
    main()
