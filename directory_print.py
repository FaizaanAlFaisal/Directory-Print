import os
import fnmatch
import argparse
from pathlib import Path


def load_gitignore_patterns(target_dir):
    """
    Load and parse .gitignore from the target directory.
    """
    gitignore_file = Path(target_dir) / ".gitignore"
    ignore_patterns = []

    if gitignore_file.exists():
        with open(gitignore_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'): # ignore blank lines and comments
                    ignore_patterns.append(line)
    
    return ignore_patterns


def is_ignored(file_path, ignore_patterns):
    """
    Check if the file matches any ignore pattern.
    """
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(file_path.name, pattern):
            return True
        
        if pattern.endswith('/') and file_path.is_dir():
            if fnmatch.fnmatch(file_path.name + '/', pattern):
                return True
        
    return False


def print_directory_structure_list(target_dir, ignore_patterns, parent_dir=''):
    """
    Print directory structure, ignoring files and dirs based on .gitignore.
    """
    target_dir = Path(target_dir)

    for item in target_dir.iterdir():
        relative_item = item.relative_to(target_dir)
        
        if is_ignored(item, ignore_patterns):
            continue

        print(os.path.join(parent_dir, str(relative_item)))
        
        if item.is_dir():
            print_directory_structure_list(item, ignore_patterns, parent_dir=os.path.join(parent_dir, str(relative_item)))


def print_directory_structure_tree(target_dir, ignore_patterns, parent_dir='', prefix=''):
    """
    Print directory structure as an ASCII tree, ignoring files and dirs based on .gitignore.
    """
    target_dir = Path(target_dir)

    for idx, item in enumerate(target_dir.iterdir()):
        relative_item = item.relative_to(target_dir)

        if is_ignored(item, ignore_patterns):
            continue

        if idx == len(list(target_dir.iterdir())) - 1:  # if last item
            print(f"{prefix}└── {relative_item}")
            new_prefix = prefix + "    "
        else:
            print(f"{prefix}├── {relative_item}")
            new_prefix = prefix + "│   "

        if item.is_dir():
            print_directory_structure_tree(item, ignore_patterns, parent_dir=os.path.join(parent_dir, str(relative_item)), prefix=new_prefix)


def main(target_dir, output_format):
    ignore_patterns = load_gitignore_patterns(target_dir)
    
    if output_format == "list":
        print_directory_structure_list(target_dir, ignore_patterns)
    elif output_format == "tree":
        print_directory_structure_tree(target_dir, ignore_patterns)


if __name__ == "__main__":
    # set up command line arguments
    parser = argparse.ArgumentParser(description="Print the directory structure while ignoring files and directories specified in .gitignore")
    parser.add_argument('target_dir', metavar='TARGET_DIR', type=str, help="The target directory to scan")
    parser.add_argument('--output', choices=['list', 'tree'], default='tree', help="Specify the output format: 'list' or 'tree' (default: 'tree')")
    
    # parse
    args = parser.parse_args()
    
    main(args.target_dir, args.output)