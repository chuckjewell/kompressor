# Kompressor

Kompressor is a Python script that generates a comprehensive overview of a project by compiling all README.md files and code files with specified extensions into a single output file. It's designed to provide a quick and easy way to create a complete picture of a project for analysis by Large Language Models (LLMs) or for human review.

## Features

- Includes all README.md files found in the project directory and its subfolders
- Supports multiple file extensions for code files
- Customizable output file name
- Clear separation and labeling of different files in the output
- Comprehensive error handling for production use

## Installation

1. Ensure you have Python 3.6 or higher installed on your system.
2. Clone this repository or download the `kompressor.py` script.

## Usage

Run Kompressor from the command line with the following syntax:

```
python kompressor.py [-h] [-e EXTENSIONS [EXTENSIONS ...]] [-d DIRECTORY] [-o OUTPUT]
```

### Arguments

- `-h, --help`: Show the help message and exit
- `-e EXTENSIONS [EXTENSIONS ...], --extensions EXTENSIONS [EXTENSIONS ...]`: File extensions to include (default: .py). For multiple extensions, separate with spaces. README.md files are always included.
- `-d DIRECTORY, --directory DIRECTORY`: Root directory of the code (default: current directory). All subfolders will be searched for README.md files and specified file types.
- `-o OUTPUT, --output OUTPUT`: Output file name (default: kompressor_output.txt)

### Examples

1. Default usage (Python files and all READMEs from all subfolders in current directory, output to kompressor_output.txt):

   ```
   python kompressor.py
   ```

2. Specify a single extension:

   ```
   python kompressor.py -e py
   ```

3. Specify multiple extensions:

   ```
   python kompressor.py -e py js css
   ```

4. Specify directory and output file:

   ```
   python kompressor.py -d /path/to/project -o project_overview.txt
   ```

5. Combine all options:
   ```
   python kompressor.py -e py js css -d /path/to/project -o project_overview.txt
   ```

## Output

Kompressor generates a single text file containing:

1. An explanation header describing the contents of the file
2. All README.md files found in the project directory and its subfolders
3. All code files with the specified extensions

Each file in the output is clearly labeled with its relative path in the project structure.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions to Kompressor are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any problems or have any questions about Kompressor, please open an issue in the GitHub repository.
