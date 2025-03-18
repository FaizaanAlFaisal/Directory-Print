import os
import fnmatch
import argparse
from pathlib import Path


def load_gitignore_patterns(target_dir, use_gitignore):
    """
    Load and parse .gitignore from the target directory.
    """
    gitignore_file = Path(target_dir) / ".gitignore"
    ignore_patterns = []

    if gitignore_file.exists() and use_gitignore:
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


def print_directory_structure_list(target_dir, ignore_patterns, parent_dir='', show_ignored_dirs=False):
    """
    Print directory structure, ignoring files and dirs based on .gitignore.
    """
    target_dir = Path(target_dir)

    for item in target_dir.iterdir():
        relative_item = item.relative_to(target_dir)

        if item.is_dir():
            relative_item = relative_item.as_posix() + '/'
                    
        if is_ignored(item, ignore_patterns):
            if item.is_dir() and show_ignored_dirs: # show ignored dir heads if needed
                print(os.path.join(parent_dir, str(relative_item)))
            continue

        print(os.path.join(parent_dir, str(relative_item)))
        
        if item.is_dir():
            print_directory_structure_list(item, ignore_patterns, parent_dir=os.path.join(parent_dir, str(relative_item)), show_ignored_dirs=show_ignored_dirs)


def print_directory_structure_tree(target_dir, ignore_patterns, parent_dir='', prefix='', show_ignored_dirs=False):
    """
    Print directory structure as an ASCII tree, ignoring files and dirs based on .gitignore.
    """
    target_dir = Path(target_dir)

    for idx, item in enumerate(target_dir.iterdir()):
        relative_item = item.relative_to(target_dir)
        
        if item.is_dir():
            relative_item = relative_item.as_posix() + '/'

        if is_ignored(item, ignore_patterns):
            if item.is_dir() and show_ignored_dirs: # show ignored dir heads if needed
                if idx == len(list(target_dir.iterdir())) - 1:
                    print(f"{prefix}└── {relative_item}")
                else:
                    print(f"{prefix}├── {relative_item}")
            continue

        if idx == len(list(target_dir.iterdir())) - 1:  # if last item
            print(f"{prefix}└── {relative_item}")
            new_prefix = prefix + "    "
        else:
            print(f"{prefix}├── {relative_item}")
            new_prefix = prefix + "│   "

        if item.is_dir():
            print_directory_structure_tree(item, ignore_patterns, parent_dir=os.path.join(parent_dir, str(relative_item)), prefix=new_prefix, show_ignored_dirs=show_ignored_dirs)


def main(target_dir, output_format, manual_ignore_patterns, use_gitignore, show_ignored_dirs):
    ignore_patterns = load_gitignore_patterns(target_dir, use_gitignore)

    if manual_ignore_patterns:
        ignore_patterns.extend(manual_ignore_patterns)
    
    if output_format == "list":
        print_directory_structure_list(target_dir, ignore_patterns, show_ignored_dirs=show_ignored_dirs)
    elif output_format == "tree":
        print_directory_structure_tree(target_dir, ignore_patterns, show_ignored_dirs=show_ignored_dirs)


if __name__ == "__main__":
    # set up command line arguments
    parser = argparse.ArgumentParser(description="Print the directory structure while ignoring files and directories specified in .gitignore")
    parser.add_argument('target_dir', metavar='TARGET_DIR', type=str, help="The target directory to scan")
    parser.add_argument('--output', choices=['list', 'tree'], default='tree', help="Specify the output format: 'list' or 'tree' (default: 'tree')")
    parser.add_argument('--ignore', type=str, help="Comma-separated list of additional files or directories to ignore. e.g. '--ignore=.env,.git'")
    parser.add_argument('--use_gitignore', type=str, default="True", choices=['True', 'False'],
                        help="Specify whether to use the .gitignore file (default: True). e.g. '--use_gitignore=False'")
    parser.add_argument('--show_ignored_dirs', action='store_true', help="Show ignored directories (default: False)")

    # parse
    args = parser.parse_args()
    
    use_gitignore = False if args.use_gitignore == 'False' else True

    manual_ignore_patterns = []
    if args.ignore:
        manual_ignore_patterns = [pattern.strip() for pattern in args.ignore.split(',')]

    if not os.path.exists(args.target_dir):
       raise ValueError(f"Error: {args.target_dir} does not exist.")
    
    if not os.path.isdir(args.target_dir):
        raise ValueError(f"Error: {args.target_dir} is not a directory.")
    
    if args.output != "list" and args.output != "tree":
        raise ValueError(f"Error: Invalid output format '{args.output}'. Please specify 'list' or 'tree'.") 

    print(f"Target Directory: {args.target_dir}")
    print(f"Output Format: {args.output}")
    print(f"Additional Ignored Files: {args.ignore}")
    print(f"Using .gitignore: {args.use_gitignore}")
    print(f"Show Ignored Directories: {args.show_ignored_dirs}")
    print("\n\n")

    main(args.target_dir, args.output, manual_ignore_patterns, use_gitignore, args.show_ignored_dirs)