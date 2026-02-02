from pathlib import Path
import csv

from filename_parser import (
    describe_drawing,
    get_tank_number,
    get_drawing_code,
    code_packages,
)

from sorters import panel_type_grouped
from groupers import document_group
from config import CSV_DELIMITER, PACKAGES


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"
OUTPUT_DIR = PROJECT_ROOT / "output"
REVISION_CSV = PROJECT_ROOT / "data" / "revisions.csv"

EXTENSIONS = {".pdf", ".tex", ".rvt"}

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
# Helpers
# ---------------------------------------------------------------------------

def escape_latex(text: str) -> str:
    """Escape LaTeX special characters."""
    for char, replacement in LATEX_SPECIAL_CHARS.items():
        text = text.replace(char, replacement)
    return text


def get_documents(folder: Path):
    """Return all valid document files in folder."""
    if not folder.exists():
        print(f"Warning: document folder not found: {folder}")
        return []

    return sorted(
        f for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in EXTENSIONS
    )


def load_revision_data(csv_path: Path) -> dict:
    """Load revision metadata keyed by drawing_id."""
    if not csv_path.exists():
        return {}

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=CSV_DELIMITER)

        if "drawing_id" not in reader.fieldnames:
            raise ValueError(
                f"CSV header mismatch in {csv_path}. "
                f"Found: {reader.fieldnames}"
            )

        return {row["drawing_id"]: row for row in reader}


def sort_key(file: Path):
    """
    Sorting strategy:
    1) group blocks (plan/views, element drawings, models, misc/calcs/docs)
    2) for element drawings, use your panel_type_grouped ordering
    3) fallback to filename
    """
    g = document_group(file)

    # Element drawings: apply the grouped type sorter
    if g == 2:
        return (g, panel_type_grouped(file), file.name)

    # Everything else: stable alphabetical
    return (g, file.name)


# ---------------------------------------------------------------------------
# LaTeX output
# ---------------------------------------------------------------------------

def write_latex_list(files, output_file: Path, revisions: dict, title: str):
    """Write a compact LaTeX drawing list table."""
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

    # Route files into packages (NOW supports numeric + alphanumeric codes)
    for file in files:
        code = get_drawing_code(file.name)
        for pkg in code_packages(code):
            if pkg in package_files:
                package_files[pkg].append(file)

    # Generate outputs per package
    for pkg, pkg_files in package_files.items():

        # Tank 00 only (but ALL document types)
        filtered = [
            f for f in pkg_files
            if get_tank_number(f.name) == "General"
        ]

        filtered = sorted(filtered, key=sort_key)

        out = OUTPUT_DIR / f"document_list_{pkg}.tex"
        title = PACKAGES[pkg]["title"]

        write_latex_list(filtered, out, revisions, title)
        print(f"Wrote {len(filtered)} documents to {out}")


if __name__ == "__main__":
    main()
