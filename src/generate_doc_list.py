import argparse
from pathlib import Path
import csv

from filename_parser import (
    describe_drawing,
    get_tank_number,
    get_drawing_code,
    category_is_element_based,
    code_packages,
)

from sorters import panel_type_grouped
from config import CSV_DELIMITER, PACKAGES


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

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
    1) non-element-based numeric drawings
    2) element-based numeric drawings
    3) alphanumeric categories (D/C/M/P)
    4) fallback to filename
    """
    code = get_drawing_code(file.name)

    if code.isdigit():
        category = code[:2]
        element_based = category_is_element_based(category)
        section = 1 if element_based else 0

        if element_based:
            return (section, panel_type_grouped(file), file.name)

        return (section, category, code, file.name)

    if len(code) == 4 and code[0].isalpha() and code[1:].isdigit():
        if code.startswith("M"):
            return (2, code, file.name)
        return (3, code, file.name)

    return (4, file.name)


# ---------------------------------------------------------------------------
# LaTeX output
# ---------------------------------------------------------------------------

def write_latex_list(sections, output_file: Path, revisions: dict, title: str):
    """Write a compact LaTeX drawing list table."""
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as f:
        f.write("% Auto-generated file — do not edit manually\n")
        f.write("\\begin{tabularx}{\\textwidth}{l l X l l l}\n")
        f.write("\\hline\n")
        f.write("Filename & Ext. & Description & Rev & Issue date & Status \\\\\n")

        def write_group_header(label: str) -> None:
            f.write("\\hline\n")
            f.write(
                f"\\multicolumn{{6}}{{l}}{{\\textbf{{{escape_latex(label)}}}}} \\\\\n"
            )
            f.write("\\noalign{\\vspace{4pt}}\n")

        def write_section_header(label: str) -> None:
            f.write("\\hline\n")
            f.write(
                f"\\multicolumn{{6}}{{l}}{{\\textbf{{{escape_latex(label)}}}}} \\\\\n"
            )
            f.write("\\noalign{\\vspace{4pt}}\n")

        row_index = 1

        for group_label, group_files in sections:
            write_group_header(group_label)
            current_section = None
            row_index = 1

            for file in group_files:
                drawing_id = file.stem.split("_", 1)[0]
                code = get_drawing_code(file.name)
                if code.isdigit():
                    category = code[:2]
                    element_based = category_is_element_based(category)
                    section = (
                        "Panel drawings"
                        if element_based
                        else "Plan views & sections"
                    )
                else:
                    if code.startswith("M"):
                        section = "3D models"
                    else:
                        section = "Documents, calculation & misc."

                if section != current_section:
                    write_section_header(section)
                    current_section = section
                    row_index = 1

                revision = revisions.get(drawing_id, {})

                description = describe_drawing(file.name)

                rev = revision.get("rev", "-") or "-"
                issue_date = revision.get("issue_date", "-") or "-"
                status = revision.get("status", "-") or "-"
                extension = file.suffix.lstrip(".").lower()

                row_index += 1
                if row_index % 2:
                    f.write("\\rowcolor{gray!10}\n")

                f.write(
                    f"{escape_latex(drawing_id)} & "
                    f"{escape_latex(extension)} & "
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

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate LaTeX drawing/document lists from a document folder."
    )
    parser.add_argument(
        "--documents-dir",
        type=Path,
        default=PROJECT_ROOT / "data" / "documents",
        help="Folder containing drawing/document files.",
    )
    parser.add_argument(
        "--revisions-csv",
        type=Path,
        default=PROJECT_ROOT / "data" / "revisions.csv",
        help="Path to revisions CSV metadata file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "output",
        help="Folder where generated .tex lists are written.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    documents_dir = args.documents_dir.expanduser().resolve()
    revisions_csv = args.revisions_csv.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()

    files = get_documents(documents_dir)
    revisions = load_revision_data(revisions_csv)

    package_files = {pkg: [] for pkg in PACKAGES}

    # Route files into packages (NOW supports numeric + alphanumeric codes)
    for file in files:
        code = get_drawing_code(file.name)
        for pkg in code_packages(code):
            if pkg in package_files:
                package_files[pkg].append(file)

    # Generate outputs per package
    for pkg, pkg_files in package_files.items():
        files_by_tank = {}
        for file in pkg_files:
            tank = get_tank_number(file.name)
            files_by_tank.setdefault(tank, []).append(file)

        sections = []

        general_files = sorted(files_by_tank.pop("General", []), key=sort_key)
        if general_files:
            sections.append(("General (Tank 00)", general_files))

        def tank_sort_key(tank_code: str):
            if tank_code.isdigit():
                return (0, int(tank_code))
            return (1, tank_code)

        for tank in sorted(files_by_tank.keys(), key=tank_sort_key):
            tank_files = sorted(files_by_tank[tank], key=sort_key)
            if not tank_files:
                continue
            if tank.isdigit():
                label = f"Tank {tank}"
            else:
                label = f"Tank {tank}"
            sections.append((label, tank_files))

        out = output_dir / f"document_list_{pkg}.tex"
        title = PACKAGES[pkg]["title"]

        write_latex_list(sections, out, revisions, title)
        total = sum(len(group_files) for _, group_files in sections)
        print(f"Wrote {total} documents to {out}")


if __name__ == "__main__":
    main()
