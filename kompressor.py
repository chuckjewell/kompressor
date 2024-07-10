import os
import argparse
import sys
import fnmatch
import re

def parse_gitignore(root_dir):
    """
    Parse the .gitignore file and return a list of ignore patterns.
    """
    gitignore_path = os.path.join(root_dir, '.gitignore')
    ignore_patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as gitignore_file:
            for line in gitignore_file:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Convert .gitignore pattern to regex
                    pattern = re.escape(line).replace(r'\*', '.*').replace(r'\?', '.')
                    if not line.startswith('/'):
                        pattern = f'(.*/)?{pattern}'
                    if line.endswith('/'):
                        pattern += '(/.*)?'
                    ignore_patterns.append(re.compile(pattern))
    return ignore_patterns

def should_ignore(path, root_dir, ignore_patterns):
    """
    Check if a path should be ignored based on .gitignore patterns.
    """
    rel_path = os.path.relpath(path, root_dir)
    for pattern in ignore_patterns:
        if pattern.match(rel_path):
            return True
    return False

def walk_code_tree(root_dir, output_file, extensions):
    """
    Walk through the code tree starting from root_dir, gather all code files with specified extensions,
    all README.md files from all subfolders, and their contents, and write them into a single output file with appropriate headers.
    Ignore files and directories specified in .gitignore.
    """
    ignore_patterns = parse_gitignore(root_dir)

    try:
        with open(output_file, 'w', encoding='utf-8') as out:
            # Write the explanation header
            out.write(
                "This file contains a complete project wrapped up into a single file for the purpose\n"
                "of providing an overview to an LLM (Large Language Model). Each section in this file\n"
                "represents a separate file from the project. The sections include all README.md files found in any subfolder,\n"
                f"and all files with the following extensions: {', '.join(extensions)}, with headers explaining their place in the codebase.\n"
                "Files and directories specified in .gitignore have been ignored.\n"
                "Please treat each section as an individual file in the actual code tree.\n\n"
            )

            # Walk through the directory tree
            for dirpath, dirnames, filenames in os.walk(root_dir):
                # Remove ignored directories
                dirnames[:] = [d for d in dirnames if not should_ignore(os.path.join(dirpath, d), root_dir, ignore_patterns)]

                # Process README.md files first
                if 'README.md' in filenames and not should_ignore(os.path.join(dirpath, 'README.md'), root_dir, ignore_patterns):
                    readme_path = os.path.join(dirpath, 'README.md')
                    relative_path = os.path.relpath(readme_path, root_dir)
                    try:
                        with open(readme_path, 'r', encoding='utf-8') as readme:
                            out.write(f"## README: {relative_path}\n")
                            out.write(readme.read())
                            out.write("\n\n")
                    except IOError as e:
                        print(f"Error reading {readme_path}: {e}", file=sys.stderr)

                # Process other files with specified extensions
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    if (filename != 'README.md' and 
                        any(filename.endswith(ext) for ext in extensions) and 
                        not should_ignore(file_path, root_dir, ignore_patterns)):
                        relative_path = os.path.relpath(file_path, root_dir)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as code_file:
                                out.write(f"## File: {relative_path}\n")
                                out.write(code_file.read())
                                out.write("\n\n")
                        except IOError as e:
                            print(f"Error reading {file_path}: {e}", file=sys.stderr)

    except IOError as e:
        print(f"Error writing to output file {output_file}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Kompressor: Generate a code overview file for a project, including all README.md files from all subfolders.",
        epilog="""
Examples:
  # Default usage (Python files and all READMEs from all subfolders in current directory, output to kompressor_output.txt)
  python kompressor.py

  # Single extension
  python kompressor.py -e py

  # Multiple extensions
  python kompressor.py -e py js css

  # Specify directory and output file
  python kompressor.py -d /path/to/project -o project_overview.txt

  # Combine all options
  python kompressor.py -e py js css -d /path/to/project -o project_overview.txt

Note: Kompressor will include all README.md files found in the specified directory and all of its subfolders,
along with the files matching the specified extensions. Files and directories specified in .gitignore will be ignored.
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-e', '--extensions', nargs='+', default=['.py'],
                        help="File extensions to include (default: .py). For multiple extensions, separate with spaces. README.md files are always included.")
    parser.add_argument('-d', '--directory', default='.',
                        help="Root directory of the code (default: current directory). All subfolders will be searched for README.md files and specified file types.")
    parser.add_argument('-o', '--output', default='kompressor_output.txt',
                        help="Output file name (default: kompressor_output.txt)")

    args = parser.parse_args()

    # Ensure extensions start with a dot
    extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in args.extensions]

    try:
        # Walk the code tree and generate the overview file
        walk_code_tree(args.directory, args.output, extensions)
        print(f"Kompressor has written the code overview to {args.output}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()