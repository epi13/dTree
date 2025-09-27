#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

"""
Directory Tree Exporter © 2025 Poor Louis Labs

Generate a flat file list and an ASCII directory tree for a given path, with
output as Markdown, JSON, or both.

This module is CLI-compatible and supports optional input/output arguments.
"""
import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Optional


# Constants
DEFAULT_JSON_FILENAME = "dtree.json"
DEFAULT_MD_FILENAME = "dtree_tree.md"
MD_HEADER = "# Directory Tree"
MD_CODE_BLOCK_START = "```text"
MD_CODE_BLOCK_END = "```"


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a flat file list and an ASCII directory tree for a given path.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dtree.py                                    # Creates dtree.json and dtree_tree.md in current directory
  python dtree.py --format md                        # Creates only dtree_tree.md in current directory
  python dtree.py --input ./src --output ./tree.md --format md
  python dtree.py --input ./src --output ./files.json --format json
  python dtree.py --input ./src --output ./exports --format both
        """
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path.cwd(),
        help="Path to input directory or file (default: current directory)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Path to write output (file or directory). Defaults to current directory if omitted."
    )
    parser.add_argument(
        "--format",
        choices=["md", "json", "both"],
        default="both",
        help="Output format: 'md', 'json', or 'both' (default: 'both')"
    )
    return parser.parse_args()


def build_file_list(base: Path) -> List[str]:
    """Return a sorted list of all files under *base* (relative paths), including the base directory as the root."""
    # Resolve the base path to handle relative paths correctly
    base = base.resolve()

    file_paths = []
    try:
        if base.is_file():
            # If input is a file, just return that file
            file_paths.append(f"{base.parent.name}/{base.name}")
        else:
            # Input is a directory, walk through it
            for root, _, files in os.walk(base):
                for f in files:
                    full = Path(root) / f
                    # Prepend the base directory name to the relative path
                    rel_path = Path(base.name) / full.relative_to(base)
                    file_paths.append(rel_path.as_posix())
    except (OSError, PermissionError) as e:
        print(f"Error accessing {base}: {e}", file=sys.stderr)
        sys.exit(1)

    file_paths.sort()
    return file_paths

def build_tree(base: Path) -> str:
    """Return a string with an ASCII tree for the directory *base*, including the base directory as the root."""
    # Resolve the base path to handle relative paths correctly
    base = base.resolve()

    def _tree(dir_path: Path, prefix: str = "") -> List[str]:
        try:
            entries = sorted(dir_path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        except (OSError, PermissionError) as e:
            print(f"Warning: Could not read directory {dir_path}: {e}", file=sys.stderr)
            return [f"{prefix}├── [Permission denied]"]

        lines = []
        for i, entry in enumerate(entries):
            connector = "└── " if i == len(entries) - 1 else "├── "
            if entry.is_dir():
                lines.append(f"{prefix}{connector}{entry.name}/")
                extension = "    " if i == len(entries) - 1 else "│   "
                lines.extend(_tree(entry, prefix + extension))
            else:
                lines.append(f"{prefix}{connector}{entry.name}")
        return lines

    try:
        if base.is_file():
            # If input is a file, show just that file
            return f"{base.parent.name}/\n└── {base.name}"
        else:
            # Add the base directory as the root
            tree_lines = [f"{base.name}/"]
            tree_lines.extend(_tree(base))
            return "\n".join(tree_lines)
    except (OSError, PermissionError) as e:
        print(f"Error building tree for {base}: {e}", file=sys.stderr)
        sys.exit(1)


def write_json(output: Path, files: List[str]) -> None:
    """Write the file list to a JSON file."""
    try:
        with output.open("w", encoding="utf-8") as f:
            json.dump({"files": files}, f, indent=2)
    except (OSError, PermissionError) as e:
        print(f"Error writing JSON to {output}: {e}", file=sys.stderr)
        sys.exit(1)


def write_tree_md(output: Path, tree_str: str) -> None:
    """Write the directory tree to a Markdown file."""
    try:
        with output.open("w", encoding="utf-8") as f:
            f.write(f"{MD_HEADER}\n\n")
            f.write(f"{MD_CODE_BLOCK_START}\n")
            f.write(tree_str)
            f.write(f"\n{MD_CODE_BLOCK_END}")
    except (OSError, PermissionError) as e:
        print(f"Error writing Markdown to {output}: {e}", file=sys.stderr)
        sys.exit(1)

def validate_input_path(input_path: Path) -> None:
    """Validate that the input path exists and is accessible."""
    if not input_path.exists():
        print(f"Error: Input path '{input_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    try:
        input_path.resolve()  # Check if path is accessible
    except (OSError, PermissionError) as e:
        print(f"Error: Cannot access input path '{input_path}': {e}", file=sys.stderr)
        sys.exit(1)


def determine_output_paths(output: Optional[Path], format_type: str) -> tuple[Optional[Path], Optional[Path]]:
    """Determine the output file paths based on format and output destination."""
    if output is None:
        return None, None  # STDOUT

    try:
        output.parent.mkdir(parents=True, exist_ok=True)
    except (OSError, PermissionError) as e:
        print(f"Error: Cannot create output directory '{output.parent}': {e}", file=sys.stderr)
        sys.exit(1)

    if output.is_dir() or format_type == "both":
        # Output directory specified or format is both
        if not output.is_dir():
            try:
                output.mkdir(parents=True, exist_ok=True)
            except (OSError, PermissionError) as e:
                print(f"Error: Cannot create output directory '{output}': {e}", file=sys.stderr)
                sys.exit(1)
        json_output = output / DEFAULT_JSON_FILENAME
        md_output = output / DEFAULT_MD_FILENAME
    else:
        # Output file specified
        if format_type == "json":
            json_output = output
            md_output = None
        elif format_type == "md":
            json_output = None
            md_output = output
        else:  # This shouldn't happen due to argparse choices
            json_output = None
            md_output = None

    return json_output, md_output


def output_to_stdout(files: List[str], tree_str: str, format_type: str) -> None:
    """Output the results to STDOUT."""
    if format_type in ("md", "both"):
        print(f"{MD_HEADER}\n\n{MD_CODE_BLOCK_START}")
        print(tree_str)
        print(MD_CODE_BLOCK_END)
    if format_type in ("json", "both"):
        if format_type == "both":
            print()  # Add spacing
        print(json.dumps({"files": files}, indent=2))


def output_to_files(json_output: Optional[Path], md_output: Optional[Path],
                   files: List[str], tree_str: str, format_type: str) -> None:
    """Output the results to files."""
    if json_output and format_type in ("json", "both"):
        write_json(json_output, files)
        print(f"JSON saved to {json_output}")

    if md_output and format_type in ("md", "both"):
        write_tree_md(md_output, tree_str)
        print(f"Tree saved to {md_output}")


def main() -> None:
    """Main function to generate directory tree and file list based on command-line arguments."""
    args = parse_arguments()

    validate_input_path(args.input)

    # Build data
    files = build_file_list(args.input)
    tree_str = build_tree(args.input)

    # Determine output paths
    if args.output is None:
        # Default to current directory when no output specified
        args.output = Path.cwd()

    json_output, md_output = determine_output_paths(args.output, args.format)

    # Always output to files (either specified location or current directory)
    output_to_files(json_output, md_output, files, tree_str, args.format)


if __name__ == "__main__":
    main()
