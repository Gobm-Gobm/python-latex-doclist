from pathlib import Path
from filename_parser import (
    describe_drawing,
    get_tank_number,
    get_drawing_code,
    category_packages,
    get_category_code, 
)
import csv
from config import CSV_DELIMITER, PACKAGES




# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Folder containing input documents to be listed in the report
DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"

# Output LaTeX file (this file is generated automatically)
OUTPUT_FILE = PROJECT_ROOT / "output" / "document_list.tex"

# Folder containing csv file for revisions & date
REVISION_CSV = PROJECT_ROOT / "data" / "revisions.csv"

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

def load_revision_data(csv_path):
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=CSV_DELIMITER)

        if "drawing_id" not in reader.fieldnames:
            raise ValueError(
                f"CSV header mismatch in {csv_path}. "
                f"Found: {reader.fieldnames}. "
                f"Check delimiter or CSV format."
            )

        return {row["drawing_id"]: row for row in reader}


def write_latex_list(files, output_file: Path, revisions: dict, title: str):
    """
    Write a compact, readable LaTeX drawing list table.

    Columns:
    Filename | Description | Rev | Issue date | Status
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as f:
        f.write("% Auto-generated file — do not edit manually\n")
        f.write(f"\\section*{{{title}}}\n")

        f.write("\\begin{tabularx}{\\textwidth}{X X l l l}\n")
        f.write("\\hline\n")
        f.write("Filename & Description & Rev & Issue date & Status \\\\\n")
        f.write("\\hline\n")

        for file in files:
            drawing_id = file.stem
            revision = revisions.get(drawing_id, {})

            description = describe_drawing(file.name)

            rev = revision.get("rev", "-") or "-"
            issue_date = revision.get("issue_date", "-") or "-"
            status = revision.get("status", "-") or "-"

            f.write(
                f"{escape_latex(file.name)} & "
                f"{escape_latex(description)} & "
                f"{escape_latex(rev)} & "
                f"{escape_latex(issue_date)} & "
                f"{escape_latex(status)} \\\\\n"
            )

        f.write("\\hline\n")
        f.write("\\end{tabularx}\n")

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    files = get_documents(DOCUMENTS_DIR)
    revisions = load_revision_data(REVISION_CSV)

    package_files = {pkg: [] for pkg in PACKAGES}

    for file in files:
        cat = get_category_code(file.name)
        for pkg in category_packages(cat):
            if pkg in package_files:
                package_files[pkg].append(file)

    for pkg, pkg_files in package_files.items():
        out = PROJECT_ROOT / "output" / f"document_list_{pkg}.tex"
        title = PACKAGES[pkg]["title"]
        write_latex_list(pkg_files, out, revisions, title)
        print(f"Wrote {len(pkg_files)} documents to {out}")


# Run the script only when executed directly (not when imported)
if __name__ == "__main__":
    main()
