import os
import argparse
import sys


def walk_code_tree(root_dir, output_file, extensions):
    """
    Walk through the code tree starting from root_dir, gather all code files with specified extensions,
    all README.md files from all subfolders, and their contents, and write them into a single output file with appropriate headers.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as out:
            # Write the explanation header
            out.write(
                "This file contains a complete project wrapped up into a single file for the purpose\n"
                "of providing an overview to an LLM (Large Language Model). Each section in this file\n"
                "represents a separate file from the project. The sections include all README.md files found in any subfolder,\n"
                f"and all files with the following extensions: {', '.join(extensions)}, with headers explaining their place in the codebase.\n"
                "Please treat each section as an individual file in the actual code tree.\n\n"
            )

            # Walk through the directory tree
            for dirpath, dirnames, filenames in os.walk(root_dir):
                # Process README.md files first
                if 'README.md' in filenames:
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
                    if filename != 'README.md' and any(filename.endswith(ext) for ext in extensions):
                        file_path = os.path.join(dirpath, filename)
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
along with the files matching the specified extensions.
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
