# Directory Structure Printer

A Python script to print the directory structure while respecting `.gitignore` and other manually-specified ignore patterns. It supports both list and tree formats.

## Features

- Prints directory structure (list or tree).
- Respects `.gitignore` and manual ignore patterns.
- Option to show ignored directories.

## Usage

Assuming that terminal is in same directory as directory_print.py:
```bash
python directory_print.py FULL_PATH_TO_TARGET_DIR
```

There are also several included options:

- `--output`: Choose list or tree (default: tree). Usage: `--output=list`
- `--ignore`: Additional files/directories to ignore (comma-separated). `--ignore=.git,node_modules`.
- `--use_gitignore`: Use .gitignore (default: True). Usage: `--use_gitignore=False`.
- `--show_ignored_dirs`: Show ignored directories (default: off). Usage: `--show_ignored_dirs`.


### Example

```bash
python directory_print.py TARGET_DIR --ignore=.git,.venv --use_gitignore=False --show_ignored_dirs
```


## Requirements

- Python 3.x
- No additional dependencies