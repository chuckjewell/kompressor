# Kompressor

Kompressor is a Python script that generates a comprehensive overview of a project by compiling all `README.md` files and code files with specified extensions into a single output file. It's designed to provide a quick and easy way to create a complete picture of a project for analysis by Large Language Models (LLMs) or for human review.

## **Features**

- **Includes all `README.md` files** found in the project directory and its subfolders.
- **Supports multiple file extensions** for code files, customizable via command-line arguments.
- **Framework-specific presets** for popular frameworks (e.g., React, Django, WordPress) with default extensions and ignore patterns.
- **Customizable output file name** and root directory.
- **Allows additional extensions and ignore patterns** to fine-tune presets or customize from scratch.
- **Clear separation and labeling** of different files in the output, preserving the project structure.
- **Respects `.gitignore` patterns**, excluding files and directories specified in `.gitignore`.
- **No external dependencies required**, works with standard Python libraries.
- **Comprehensive error handling** for production use.

## **Installation**

1. Ensure you have **Python 3.6 or higher** installed on your system.
2. Download the `kompressor.py` script and place it in your desired directory.

## **Usage**

Run Kompressor from the command line with the following syntax:

```bash
python kompressor.py [-h] [-e EXTENSIONS [EXTENSIONS ...]] [-d DIRECTORY] [-o OUTPUT] [--ignore IGNORE [IGNORE ...]] [preset options]
```

### **Arguments**

- `-h, --help`: Show the help message and exit.
- `-e EXTENSIONS [EXTENSIONS ...], --extensions EXTENSIONS [EXTENSIONS ...]`: File extensions to include **in addition to the defaults**. For multiple extensions, separate with spaces. `README.md` files are always included.
- `-d DIRECTORY, --directory DIRECTORY`: Root directory of the code (default: current directory). All subfolders will be searched for `README.md` files and specified file types.
- `-o OUTPUT, --output OUTPUT`: Output file name (default: `kompressor_output.txt`).
- `--ignore IGNORE [IGNORE ...]`: Additional files, directories, or patterns to ignore. For multiple patterns, separate with spaces.

### **Framework Preset Options**

**Only one preset can be selected at a time.**

- `--remix`: Use defaults for a Remix project.
- `--nextjs`: Use defaults for a Next.js project.
- `--wordpress`: Use defaults for a WordPress project.
- `--react`: Use defaults for a React project.
- `--angular`: Use defaults for an Angular project.
- `--vue`: Use defaults for a Vue.js project.
- `--django`: Use defaults for a Django project.
- `--flask`: Use defaults for a Flask project.
- `--rails`: Use defaults for a Ruby on Rails project.
- `--laravel`: Use defaults for a Laravel project.
- `--spring`: Use defaults for a Spring Boot project.
- `--aspnet`: Use defaults for an ASP.NET project.

### **Default Extensions and Ignore Patterns for Presets**

| Preset        | Extensions                                    | Ignored Files/Directories                        |
| ------------- | --------------------------------------------- | ------------------------------------------------ |
| `--remix`     | `.ts`, `.tsx`, `.css`                         | `package-lock.json`, `yarn.lock`, `package.json` |
| `--nextjs`    | `.js`, `.jsx`, `.ts`, `.tsx`, `.css`, `.scss` | `node_modules`, `package-lock.json`, `yarn.lock` |
| `--react`     | `.js`, `.jsx`, `.ts`, `.tsx`, `.css`          | `node_modules`, `package-lock.json`, `yarn.lock` |
| `--angular`   | `.ts`, `.html`, `.css`                        | `node_modules`, `package-lock.json`, `yarn.lock` |
| `--vue`       | `.vue`, `.js`, `.ts`, `.css`                  | `node_modules`, `package-lock.json`, `yarn.lock` |
| `--wordpress` | `.php`, `.css`, `.js`                         | `node_modules`, `vendor`, `wp-config.php`        |
| `--django`    | `.py`, `.html`, `.css`                        | `venv`, `env`, `.env`, `db.sqlite3`              |
| `--flask`     | `.py`, `.html`, `.css`                        | `venv`, `env`, `.env`                            |
| `--rails`     | `.rb`, `.html.erb`, `.css`                    | `node_modules`, `vendor`, `Gemfile.lock`         |
| `--laravel`   | `.php`, `.blade.php`, `.css`                  | `node_modules`, `vendor`, `.env`                 |
| `--spring`    | `.java`, `.xml`, `.properties`                | `target`, `.classpath`, `.project`, `pom.xml`    |
| `--aspnet`    | `.cs`, `.cshtml`, `.css`                      | `bin`, `obj`, `packages`, `*.csproj`             |

### **Examples**

1. **Default usage** (Python files and all `README.md` files from all subfolders in current directory, output to `kompressor_output.txt`):

   ```bash
   python kompressor.py
   ```

2. **Specify a single extension**:

   ```bash
   python kompressor.py -e py
   ```

3. **Specify multiple extensions**:

   ```bash
   python kompressor.py -e py js css
   ```

4. **Specify directory and output file**:

   ```bash
   python kompressor.py -d /path/to/project -o project_overview.txt
   ```

5. **Combine all options**:

   ```bash
   python kompressor.py -e py js css -d /path/to/project -o project_overview.txt
   ```

6. **Use Remix project defaults with additional extensions**:

   ```bash
   python kompressor.py --remix -e json md
   ```

7. **Ignore additional files or patterns**:

   ```bash
   python kompressor.py --ignore .env secrets.txt
   ```

8. **Use a preset and add extra ignore patterns**:

   ```bash
   python kompressor.py --django --ignore db.sqlite3 .env
   ```

9. **Use a preset and fine-tune extensions**:

   ```bash
   python kompressor.py --react -e json md
   ```

10. **Specify extensions without a preset and add ignore patterns**:

    ```bash
    python kompressor.py -e py txt md --ignore secrets.txt passwords.yml
    ```

### **Notes**

- **Mutually Exclusive Presets**: Only one framework-specific preset can be selected at a time. If multiple presets are selected, the script will exit with an error.
- **Extensions Are Cumulative**: When a preset is selected, its default extensions are used, and any additional extensions provided via `-e`/`--extensions` are added to the list.
- **Ignore Patterns Are Cumulative**: The preset's default ignore files are used, and any additional patterns provided via `--ignore` are added to the list.
- **Default Behavior**: If no preset is selected and no extensions are provided, the script defaults to including `.py` files.
- **README.md Inclusion**: All `README.md` files are always included, regardless of the extensions specified.

## **Output**

Kompressor generates a single text file containing:

1. **An explanation header** describing the contents of the file.
2. **All `README.md` files** found in the project directory and its subfolders.
3. **All code files** with the specified extensions.

Each file in the output is clearly labeled with its relative path in the project structure, using headers to separate sections:

- `## README: path/to/README.md`
- `## File: path/to/file.extension`

## **How It Works**

- **Respects `.gitignore`**: The script reads the `.gitignore` file in the root directory and excludes any files or directories that match the patterns.
- **No External Dependencies**: The script is built using Python's standard library, so there's no need to install additional packages.
- **Binary File Detection**: It skips binary files by checking for null bytes, ensuring that only text files are included.
- **Error Handling**: Any errors encountered during processing are reported at the end of the script's execution.
- **Pattern Matching**: The script uses Unix shell-style wildcard pattern matching for ignore patterns.

## **Contributing**

Contributions to Kompressor are welcome! Please feel free to submit a pull request or open an issue to discuss potential changes.

### **Development Setup**

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/kompressor.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd kompressor
   ```

3. **Create a Virtual Environment (Optional)**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
   ```

4. **Run the Script**:

   ```bash
   python kompressor.py
   ```

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## **Support**

If you encounter any problems or have any questions about Kompressor, please open an issue in the GitHub repository.

## **Acknowledgments**

- Thanks to all contributors and users who have provided feedback and suggestions.
- Inspired by the need to easily compile project overviews for code analysis and reviews.

---

**By updating the `README.md`, we've ensured that all important details are covered, including:**

- **Detailed descriptions of features and how to use them.**
- **Comprehensive usage examples demonstrating different scenarios.**
- **Clear explanations of how presets and customizations work together.**
- **Notes on default behaviors and how to modify them.**
- **Information on contributing, support, and license.**

This should provide users with all the necessary information to effectively use the `kompressor.py` script and understand its capabilities.

---

**Feel free to let me know if there's anything else you'd like to add or modify!**
