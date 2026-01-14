from pathlib import Path
from filename_parser import (
    describe_drawing,
    get_tank_number,
    get_drawing_code,
)




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
    Write a LaTeX table containing the document list.
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as f:
        f.write("% Auto-generated file — do not edit manually\n")
        f.write("\\section*{Document List}\n")

        # Table header
        f.write("\\begin{tabularx}{\\textwidth}{llXlX}\n")
        f.write("\\hline\n")
        f.write("Tank & Drawing code & Filename & File type & Description \\\\\n")
        f.write("\\hline\n")

        for file in files:
            tank = get_tank_number(file.name)
            drawing_code = get_drawing_code(file.name)
            description = describe_drawing(file.name)

            safe_tank = escape_latex(tank)
            safe_code = escape_latex(drawing_code)
            safe_name = escape_latex(file.name)
            safe_description = escape_latex(description)
            file_type = file.suffix.upper().replace(".", "")

            f.write(
                f"{safe_tank} & {safe_code} & {safe_name} & "
                f"{file_type} & {safe_description} \\\\\n"
            )

        f.write("\\hline\n")
        f.write("\\end{tabularx}\n")

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
