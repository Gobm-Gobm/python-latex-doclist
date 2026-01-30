from pathlib import Path
from filename_parser import (
    describe_drawing,
    get_tank_number,
    get_drawing_code,
    get_category_code,
    category_packages,
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
OUTPUT_DIR = PROJECT_ROOT / "output"

# Folder containing csv file for revisions & dates
REVISION_CSV = PROJECT_ROOT / "data" / "revisions.csv"

# File extensions that should be treated as documents
EXTENSIONS = {
    ".pdf",   # Reports, drawings
    ".tex",   # LaTeX source documents
    ".rvt",   # Revit models
}

# Mapping of LaTeX special characters to their escaped equivalents
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
    """Escape LaTeX special characters in text."""
    for char, replacement in LATEX_SPECIAL_CHARS.items():
        text = text.replace(char, replacement)
    return text


def get_documents(folder: Path):
    """Scan the given folder and return a sorted list of document files."""
    if not folder.exists():
        print(f"Warning: document folder not found: {folder}")
        return []

    return sorted(
        f for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in EXTENSIONS
    )


def load_revision_data(csv_path: Path):
    """Load revision metadata from CSV into a lookup dictionary."""
    if not csv_path.exists():
        print(f"Warning: revision CSV not found: {csv_path}")
        return {}

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=CSV_DELIMITER)

        if "drawing_id" not in reader.fieldnames:
            raise ValueError(
                f"CSV header mismatch in {csv_path}. "
                f"Found: {reader.fieldnames}"
            )

        return {row["drawing_id"]: row for row in reader}


def base_drawing_id(filename: str) -> str:
    """
    Extract base drawing ID for revision lookup.

    Removes any descriptive suffix after the drawing code.
    """
    stem = Path(filename).stem
    return stem.split("_")[0]


def write_latex_list(files, output_file: Path, revisions: dict, title: str):
    """
    Write a compact LaTeX document list table.

    Columns:
    Filename | Description | Rev | Issue date | Status
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as f:
        f.write("% Auto-generated file — do not edit manually\n")
        f.write(f"\\section*{{{escape_latex(title)}}}\n")

        f.write("\\begin{tabularx}{\\textwidth}{X X l l l}\n")
        f.write("\\hline\n")
        f.write("Filename & Description & Rev & Issue date & Status \\\\\n")
        f.write("\\hline\n")

        for file in files:
            drawing_id = base_drawing_id(file.name)
            revision = revisions.get(drawing_id, {})

            description = describe_drawing(file.name)

            rev = revision.get("rev", "-") or "-"
            issue_date = revision.get("issue_date", "-") or "-"
            status = revision.get("status", "-") or "-"

            base_id = base_drawing_id(file.name)
            display_name = f"{base_id}{file.suffix}"

            f.write(
                f"{escape_latex(display_name)} & "
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

    # Prepare per-package file lists
    package_files = {pkg: [] for pkg in PACKAGES}

    for file in files:
        drawing_code = get_drawing_code(file.name)
        category_code = get_category_code(file.name)

        # Numeric drawing categories (DDTT)
        if category_code != "N/A":
            packages = category_packages(category_code)

        # Alphanumeric codes (Dxxx, Cxxx, Mxxx, Pxxx)
        elif drawing_code != "N/A":
            packages = PACKAGES.keys()

        else:
            packages = set()

        for pkg in packages:
            if pkg in package_files:
                package_files[pkg].append(file)

    # Write output per package
    for pkg, pkg_files in package_files.items():
        if not pkg_files:
            continue

        out = OUTPUT_DIR / f"document_list_{pkg}.tex"
        title = PACKAGES[pkg]["title"]

        write_latex_list(pkg_files, out, revisions, title)
        print(f"Wrote {len(pkg_files)} documents to {out}")


if __name__ == "__main__":
    main()
