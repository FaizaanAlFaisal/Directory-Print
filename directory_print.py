import os
from pathlib import Path
import fnmatch

def print_directory_structure(target_dir, parent_dir=''):
    target_dir = Path(target_dir)

    for item in target_dir.iterdir():
        relative_item = item.relative_to(target_dir)
        print(os.path.join(parent_dir, str(relative_item)))
        
        if item.is_dir():
            print_directory_structure(item, parent_dir=os.path.join(parent_dir, str(relative_item)))

def main(target_dir):
    print_directory_structure(target_dir)

if __name__ == "__main__":
    target_directory = input("Enter the target directory: ").strip()
    main(target_directory)
