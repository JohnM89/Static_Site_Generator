from textnode import TextNode 
from gencontent import *
import shutil
import sys
from pathlib import Path
from copystatic import copy_to_public
from genpage import generate_pages_recursive
def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
        print(basepath)
    else:
        basepath = "/"
        
    def clean_up_public_and_copy(basepath):
        cwd = Path.cwd()
        #set walk back /src/main.py to ../
        project_root = cwd

        #Path object overloads the "/" operator to join paths cleanly
        path_static = project_root / "static"
        #public for local docs for github
        path_public = project_root / "docs"
        path_content = project_root / "content"
        path_template = project_root / "template.html"
        path_to_write = path_public  
        if not path_static.exists():
            raise FileNotFoundError(f"missing source: {path_static}")
        if not path_static.is_dir():
            raise NotADirectoryError(f"source is not a directory: {path_static}")
        
        if path_public.exists() and path_public.is_dir():
            shutil.rmtree(path_public)
        path_public.mkdir()
        copy_to_public(path_static, path_public)
        generate_pages_recursive(path_content, path_template, path_to_write, basepath)
    clean_up_public_and_copy(basepath)

if __name__ == "__main__":
    main()
