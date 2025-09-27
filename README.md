# dTree
Directory Tree Exporter
# Directory Tree Exporter © 2025 Poor Louis Labs

A powerful command-line tool that generates both flat file lists and ASCII directory trees for any given path, with output in Markdown, JSON, or both formats.

## ✨ Features

- **Dual Output Formats**: Generate both structured JSON file lists and human-readable ASCII directory trees
- **Flexible Input**: Works with directories and individual files
- **Multiple Output Options**: Write to files, directories, or display to terminal
- **Type-Safe**: Comprehensive type hints throughout the codebase
- **Robust Error Handling**: Graceful handling of permissions, missing files, and edge cases
- **Zero Dependencies**: Pure Python standard library implementation

## 🚀 Quick Start

```bash
# Clone or download the repository
cd /path/to/directory

# Run with default settings (creates both JSON and Markdown files)
python dtree.py

# That's it! Check your directory for dtree.json and dtree_tree.md
```

## 📦 Installation

### Prerequisites
- Python 3.6 or higher

### Setup
1. Clone or download the repository
2. Ensure `dtree.py` is executable:
   ```bash
   chmod +x dtree.py
   ```
3. (Optional) Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

### Basic Usage

```bash
# Generate both JSON and Markdown for current directory
python dtree.py

# Generate for a specific directory
python dtree.py --input ./src

# Generate for a single file
python dtree.py --input myfile.txt
```

### Output Control

```bash
# Specify output location
python dtree.py --output ./exports

# Custom filename
python dtree.py --output tree.md --format md

# Output to specific directory
python dtree.py --output ./docs --format both
```

### Format Options

```bash
# Default: both JSON and Markdown
python dtree.py

# Markdown only
python dtree.py --format md

# JSON only
python dtree.py --format json

# Explicit both
python dtree.py --format both
```

## 🎯 Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--input PATH` | Path to directory or file to analyze | Current directory |
| `--output PATH` | Output file or directory path | Current directory |
| `--format {md,json,both}` | Output format | `both` |
| `--help` | Show help message | - |

## 📄 Output Formats

### Markdown Tree Output (dtree_tree.md)
```markdown
# Directory Tree

```
project/
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   └── test_main.py
├── README.md
└── requirements.txt
```
```

### JSON File List Output (dtree.json)
```json
{
  "files": [
    "project/src/main.py",
    "project/src/utils.py",
    "project/tests/test_main.py",
    "project/README.md",
    "project/requirements.txt"
  ]
}
```

## 🔧 Development

### Code Quality
This project maintains high code quality standards:

- **Type Hints**: Full type annotations for better IDE support and error catching
- **Error Handling**: Comprehensive error handling for edge cases
- **Code Style**: Follows PEP 8 guidelines
- **Testing**: Includes development dependencies for testing

### Running Tests
```bash
# Install development dependencies
pip install -r requirements.txt

# Run type checking
mypy dtree.py

# Format code
black dtree.py

# Lint code
flake8 dtree.py
```

### Project Structure
```
dTree/
├── dtree.py           # Main application
├── requirements.txt   # Development dependencies
└── README.md         # This file
```

## 📋 Examples

### Example 1: Analyze a Source Code Directory
```bash
python dtree.py --input ./src --output ./docs --format both
# Creates docs/dtree.json and docs/dtree_tree.md
```

### Example 2: Quick Terminal View
```bash
# View current directory structure (legacy behavior with --format md)
python dtree.py --format md
# Creates dtree_tree.md in current directory
```

### Example 3: JSON Data Export
```bash
python dtree.py --input ./data --format json --output files.json
# Creates a single JSON file with file listing
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the quality checks: `mypy dtree.py && black dtree.py && flake8 dtree.py`
5. Submit a pull request

## 📄 License

Licensed under Apache License 2.0 - see the SPDX header in `dtree.py` for details.

## 🙏 Acknowledgments

- Built with Python's excellent standard library
- Inspired by the need for better project documentation tools
- Thanks to the open source community for best practices and tools

---

**Directory Tree Exporter © 2025 Poor Louis Labs** - Making project documentation easier, one tree at a time! 🌳
