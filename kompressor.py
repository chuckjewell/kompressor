#!/usr/bin/env python3
import sys
import os
import argparse
from pathlib import Path
import re
import fnmatch


def parse_gitignore(root_dir):
    gitignore_path = root_dir / '.gitignore'
    ignore_patterns = []
    if gitignore_path.exists():
        with gitignore_path.open('r') as gitignore_file:
            for line in gitignore_file:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Handle negation patterns (skipped for simplicity)
                    if line.startswith('!'):
                        continue
                    # Convert .gitignore pattern to regex
                    pattern = fnmatch.translate(line)
                    ignore_patterns.append(re.compile(pattern))
    return ignore_patterns


def should_ignore(path, root_dir, ignore_patterns, extra_ignore_patterns):
    rel_path = path.relative_to(root_dir)
    rel_path_str = str(rel_path.as_posix())
    for pattern in ignore_patterns:
        if pattern.match(rel_path_str):
            return True
    # Check extra ignore patterns
    for pattern in extra_ignore_patterns:
        # Use fnmatch to match patterns like '*.env' or 'secrets/*'
        if fnmatch.fnmatch(rel_path_str, pattern):
            return True
    return False


def is_text_file(file_path):
    try:
        with file_path.open('rb') as f:
            chunk = f.read(1024)
            if b'\0' in chunk:
                return False  # It's a binary file
        return True
    except Exception:
        return False


def walk_code_tree(root_dir, output_file, extensions, extra_ignore_files):
    ignore_patterns = parse_gitignore(root_dir)
    errors = []

    try:
        with output_file.open('w', encoding='utf-8') as out:
            # Write the explanation header
            out.write("# Project Overview\n\n")
            out.write(
                "This file contains a complete project wrapped up into a single file for the purpose\n"
                "of providing an overview to an LLM (Large Language Model). Each section in this file\n"
                "represents a separate file from the project. The sections include all README.md files found in any subfolder,\n"
                f"and all files with the following extensions: {', '.join(extensions)}, with headers explaining their place in the codebase.\n"
                "Files and directories specified in .gitignore have been ignored.\n"
                "Please treat each section as an individual file in the actual code tree.\n\n"
            )

            for dirpath, dirnames, filenames in os.walk(root_dir):
                dirpath = Path(dirpath)
                # Remove ignored directories
                dirnames[:] = [d for d in dirnames if not should_ignore(dirpath / d, root_dir, ignore_patterns, extra_ignore_files)]

                for filename in filenames:
                    file_path = dirpath / filename
                    if should_ignore(file_path, root_dir, ignore_patterns, extra_ignore_files):
                        continue
                    if filename == 'README.md':
                        # Process README.md
                        try:
                            with file_path.open('r', encoding='utf-8', errors='ignore') as readme:
                                out.write(f"## README: {file_path.relative_to(root_dir)}\n")
                                out.write(readme.read())
                                out.write("\n\n")
                        except Exception as e:
                            errors.append(f"Error reading {file_path}: {e}")
                            print(errors[-1], file=sys.stderr)
                    elif file_path.suffix in extensions:
                        if is_text_file(file_path):
                            try:
                                with file_path.open('r', encoding='utf-8', errors='ignore') as code_file:
                                    out.write(f"## File: {file_path.relative_to(root_dir)}\n")
                                    out.write(code_file.read())
                                    out.write("\n\n")
                            except Exception as e:
                                errors.append(f"Error reading {file_path}: {e}")
                                print(errors[-1], file=sys.stderr)
        if errors:
            print("Some files could not be processed:", file=sys.stderr)
            for error in errors:
                print(error, file=sys.stderr)
    except Exception as e:
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

  # Remix project defaults
  python kompressor.py --remix

  # Next.js project defaults
  python kompressor.py --nextjs

  # WordPress project defaults
  python kompressor.py --wordpress

  # React project defaults
  python kompressor.py --react

  # Angular project defaults
  python kompressor.py --angular

  # Vue.js project defaults
  python kompressor.py --vue

  # Django project defaults
  python kompressor.py --django

  # Flask project defaults
  python kompressor.py --flask

  # Ruby on Rails project defaults
  python kompressor.py --rails

  # Laravel project defaults
  python kompressor.py --laravel

  # Spring Boot project defaults
  python kompressor.py --spring

  # ASP.NET project defaults
  python kompressor.py --aspnet

Note: Kompressor will include all README.md files found in the specified directory and all of its subfolders,
along with the files matching the specified extensions. Files and directories specified in .gitignore will be ignored.
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-e', '--extensions', nargs='+', default=[],
                        help="File extensions to include in addition to the defaults. For multiple extensions, separate with spaces. README.md files are always included.")
    parser.add_argument('-d', '--directory', default='.',
                        help="Root directory of the code (default: current directory). All subfolders will be searched for README.md files and specified file types.")
    parser.add_argument('-o', '--output', default='kompressor_output.txt',
                        help="Output file name (default: kompressor_output.txt)")
    parser.add_argument('--ignore', nargs='+', default=[],
                        help="Additional files, directories, or patterns to ignore. For multiple patterns, separate with spaces.")

    # Framework-specific options
    parser.add_argument('--remix', action='store_true',
                        help="Use default settings for a Remix project (include .ts, .tsx, .css files, ignore verbose configuration files).")
    parser.add_argument('--nextjs', action='store_true',
                        help="Use default settings for a Next.js project (include .js, .jsx, .ts, .tsx, .css, .scss files, ignore verbose configuration files).")
    parser.add_argument('--wordpress', action='store_true',
                        help="Use default settings for a WordPress project (include .php, .css, .js files, ignore verbose configuration files).")
    parser.add_argument('--django', action='store_true',
                        help="Use default settings for a Django project (include .py, .html, .css files, ignore virtual environments and database files).")
    parser.add_argument('--flask', action='store_true',
                        help="Use default settings for a Flask project (include .py, .html, .css files, ignore virtual environments and configuration files).")
    parser.add_argument('--react', action='store_true',
                        help="Use default settings for a React project (include .js, .jsx, .ts, .tsx, .css files, ignore verbose configuration files).")
    parser.add_argument('--angular', action='store_true',
                        help="Use default settings for an Angular project (include .ts, .html, .css files, ignore verbose configuration files).")
    parser.add_argument('--vue', action='store_true',
                        help="Use default settings for a Vue.js project (include .vue, .js, .ts, .css files, ignore verbose configuration files).")
    parser.add_argument('--rails', action='store_true',
                        help="Use default settings for a Ruby on Rails project (include .rb, .html.erb, .css files, ignore verbose configuration files).")
    parser.add_argument('--laravel', action='store_true',
                        help="Use default settings for a Laravel project (include .php, .blade.php, .css files, ignore verbose configuration files).")
    parser.add_argument('--spring', action='store_true',
                        help="Use default settings for a Spring Boot project (include .java, .xml, .properties files, ignore build directories).")
    parser.add_argument('--aspnet', action='store_true',
                        help="Use default settings for an ASP.NET project (include .cs, .cshtml, .css files, ignore build directories and configuration files).")

    args = parser.parse_args()

    # Handle framework-specific options
    framework_options = {
        '--remix': args.remix,
        '--nextjs': args.nextjs,
        '--wordpress': args.wordpress,
        '--django': args.django,
        '--flask': args.flask,
        '--react': args.react,
        '--angular': args.angular,
        '--vue': args.vue,
        '--rails': args.rails,
        '--laravel': args.laravel,
        '--spring': args.spring,
        '--aspnet': args.aspnet
    }
    selected_frameworks = [name for name, selected in framework_options.items() if selected]
    if len(selected_frameworks) > 1:
        print(f"Please select only one framework-specific option ({', '.join(framework_options.keys())}).", file=sys.stderr)
        sys.exit(1)

    extensions = []
    extra_ignore_patterns = []

    if args.remix:
        extensions.extend(['.ts', '.tsx', '.css'])
        extra_ignore_patterns.extend(['package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'package.json'])
    elif args.nextjs or args.react:
        extensions.extend(['.js', '.jsx', '.ts', '.tsx', '.css', '.scss'])
        extra_ignore_patterns.extend(['node_modules', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'package.json'])
    elif args.wordpress:
        extensions.extend(['.php', '.css', '.js'])
        extra_ignore_patterns.extend(['node_modules', 'vendor', 'composer.lock', 'package-lock.json', 'yarn.lock', 'wp-config.php'])
    elif args.django:
        extensions.extend(['.py', '.html', '.css'])
        extra_ignore_patterns.extend(['venv', 'env', '.env', 'db.sqlite3'])
    elif args.flask:
        extensions.extend(['.py', '.html', '.css'])
        extra_ignore_patterns.extend(['venv', 'env', '.env'])
    elif args.angular:
        extensions.extend(['.ts', '.html', '.css'])
        extra_ignore_patterns.extend(['node_modules', 'package-lock.json', 'yarn.lock', 'angular.json'])
    elif args.vue:
        extensions.extend(['.vue', '.js', '.ts', '.css'])
        extra_ignore_patterns.extend(['node_modules', 'package-lock.json', 'yarn.lock', 'vue.config.js'])
    elif args.rails:
        extensions.extend(['.rb', '.html.erb', '.css'])
        extra_ignore_patterns.extend(['node_modules', 'vendor', 'Gemfile.lock', 'package-lock.json', 'yarn.lock'])
    elif args.laravel:
        extensions.extend(['.php', '.blade.php', '.css'])
        extra_ignore_patterns.extend(['node_modules', 'vendor', 'composer.lock', 'package-lock.json', 'yarn.lock', '.env'])
    elif args.spring:
        extensions.extend(['.java', '.xml', '.properties'])
        extra_ignore_patterns.extend(['target', '.classpath', '.project', 'pom.xml'])
    elif args.aspnet:
        extensions.extend(['.cs', '.cshtml', '.css'])
        extra_ignore_patterns.extend(['bin', 'obj', 'packages', '*.csproj', 'appsettings.json'])
    else:
        # If no preset is selected and no extensions are specified, default to .py
        if not args.extensions:
            extensions.append('.py')

    # Add any additional extensions specified via -e
    # Ensure extensions start with a dot
    extensions.extend([ext if ext.startswith('.') else f'.{ext}' for ext in args.extensions])

    # Add any additional ignore patterns specified via --ignore
    extra_ignore_patterns.extend(args.ignore)

    root_dir = Path(args.directory).resolve()
    output_file = Path(args.output).resolve()

    try:
        # Walk the code tree and generate the overview file
        walk_code_tree(root_dir, output_file, extensions, extra_ignore_patterns)
        print(f"Kompressor has written the code overview to {output_file}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
