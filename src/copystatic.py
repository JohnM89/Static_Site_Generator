import shutil   
from pathlib import Path

def copy_to_public(path_static, path_public):
    if not path_static.exists():
        raise FileNotFoundError(f"missing source: {path_static}")
    if not path_static.is_dir():
        raise NotADirectoryError(f"source is not a directory {path_static}")
    
    for x in path_static.iterdir():
        dest = path_public / x.name
        if x.is_file():
            shutil.copy(x, dest)
        elif x.is_dir():
            #recursive call to build subdirectories
            dest.mkdir(exist_ok=True)
            copy_to_public(x, dest)


