from pathlib import Path
from filename_parser import describe_drawing


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Folder containing input documents to be listed in the report
DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"

# Output LaTeX file (this file is generated automatically)
OUTPUT_FILE = PROJECT_ROOT / "output" / "document_list.tex"

# File extensions that should be treated as documents
# Only files with these extensions will appear in the list
EXTENSIONS = {
    ".pdf",   # Reports, drawings
    ".tex",   # LaTeX source documents
    ".rvt",   # Revit models
}

# Mapping of LaTeX special characters to their escaped equivalents
# This prevents LaTeX compilation errors when filenames contain
# characters with special meaning in LaTeX
LATEX_SPECIAL_CHARS = {
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def escape_latex(text: str) -> str:
    """
    Escape LaTeX special characters in a string.

    This is required because filenames may contain characters (such as '_')
    that cause LaTeX compilation errors if used directly in text mode.
    """
    for char, replacement in LATEX_SPECIAL_CHARS.items():
        text = text.replace(char, replacement)
    return text


def get_documents(folder: Path):
    """
    Scan the given folder and return a sorted list of document files.
    """
    if not folder.exists():
        print(f"Warning: document folder not found: {folder}")
        return []

    return sorted(
        f for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in EXTENSIONS
    )


def write_latex_list(files, output_file: Path):
    """
    Write a LaTeX itemized list of document filenames.

    The output file is generated automatically and should not be edited
    manually, as it will be overwritten each time the script is run.
    """
    # Ensure the output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Write the LaTeX content
    with output_file.open("w", encoding="utf-8") as f:
        f.write("% Auto-generated file — do not edit manually\n")
        f.write("\\section*{Document List}\n")
        f.write("\\begin{itemize}\n")

        for file in files:
            description = describe_drawing(file.name)

            safe_name = escape_latex(file.name)
            safe_description = escape_latex(description)

            if description != "N/A":
                f.write(f"  \\item {safe_name} --- {safe_description}\n")
            else:
                f.write(f"  \\item {safe_name} --- N/A\n")
        f.write("\\end{itemize}\n")

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    """
    Main execution function.

    Collects documents from the input folder and generates the LaTeX
    document list.
    """
    files = get_documents(DOCUMENTS_DIR)
    write_latex_list(files, OUTPUT_FILE)
    print(f"Wrote {len(files)} documents to {OUTPUT_FILE}")


# Run the script only when executed directly (not when imported)
if __name__ == "__main__":
    main()
