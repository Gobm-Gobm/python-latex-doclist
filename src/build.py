import argparse
import subprocess
import shutil
import sys
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Scripts and files
DOC_LIST_SCRIPT = PROJECT_ROOT / "src" / "generate_doc_list.py"
TEX_FILES = [
    PROJECT_ROOT / "latex_build" / "test" / "report_for_client.tex",
    PROJECT_ROOT / "latex_build" / "test" / "report_for_manufacture.tex",
    PROJECT_ROOT / "latex_build" / "test" / "report_for_installation.tex",
]

# Output folders
RESULT_DIR = PROJECT_ROOT / "latex_result"
BUILD_DIR = PROJECT_ROOT / "latex_build"

LATEX_EXTENSIONS = {
    ".aux",
    ".log",
    ".out",
    ".toc",
    ".lof",
    ".lot",
    ".fls",
    ".fdb_latexmk",
    ".synctex.gz",
}

# ---------------------------------------------------------------------------
# Build steps
# ---------------------------------------------------------------------------

def generate_document_list(
    documents_dir: Optional[Path] = None,
    revisions_csv: Optional[Path] = None,
    output_dir: Optional[Path] = None,
):
    """
    Generate the LaTeX document list from files in a document folder.
    """
    print("Generating document list...")
    command = [sys.executable, DOC_LIST_SCRIPT.name]
    if documents_dir is not None:
        command.extend(["--documents-dir", str(documents_dir)])
    if revisions_csv is not None:
        command.extend(["--revisions-csv", str(revisions_csv)])
    if output_dir is not None:
        command.extend(["--output-dir", str(output_dir)])
    subprocess.run(
        command,
        cwd=DOC_LIST_SCRIPT.parent,
        check=True,
    )


def run_pdflatex(tex_file: Path, runs: int = 2):
    """
    Run pdflatex multiple times to resolve references if needed.
    """
    print("Running pdflatex...")
    for i in range(runs):
        subprocess.run(
            ["pdflatex", tex_file.name],
            cwd=tex_file.parent,
            check=True,
        )


def move_outputs(tex_file: Path, result_dir: Path):
    """
    Move the generated PDF and LaTeX build artefacts into
    their respective folders.
    """
    result_dir.mkdir(parents=True, exist_ok=True)
    BUILD_DIR.mkdir(exist_ok=True)

    base_name = tex_file.stem

    for file in tex_file.parent.iterdir():
        # Final PDF → latex_result/
        if file.suffix == ".pdf" and file.stem == base_name:
            shutil.move(str(file), result_dir / file.name)

        # Build artefacts → latex_build/
        elif file.suffix in LATEX_EXTENSIONS:
            shutil.move(str(file), BUILD_DIR / file.name)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate drawing lists and build report PDFs."
    )
    parser.add_argument(
        "--documents-dir",
        type=Path,
        help="Optional folder containing drawing/document files.",
    )
    parser.add_argument(
        "--revisions-csv",
        type=Path,
        help="Optional revisions CSV path.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Optional output folder for generated document_list_*.tex files.",
    )
    parser.add_argument(
        "--result-dir",
        type=Path,
        help="Optional output folder for generated PDFs.",
    )
    args = parser.parse_args()

    documents_dir = None
    if args.documents_dir is not None:
        documents_dir = args.documents_dir.expanduser().resolve()

    revisions_csv = None
    if args.revisions_csv is not None:
        revisions_csv = args.revisions_csv.expanduser().resolve()
    elif documents_dir is not None:
        # When using an external documents folder, default revisions next to it.
        revisions_csv = documents_dir / "revisions.csv"

    output_dir = None
    if args.output_dir is not None:
        output_dir = args.output_dir.expanduser().resolve()
    else:
        # Keep generated TeX lists in the repo output folder by default.
        output_dir = PROJECT_ROOT / "output"

    result_dir = RESULT_DIR
    if args.result_dir is not None:
        result_dir = args.result_dir.expanduser().resolve()
    elif documents_dir is not None:
        # When using an external documents folder, default PDF output next to input.
        result_dir = documents_dir

    generate_document_list(
        documents_dir=documents_dir,
        revisions_csv=revisions_csv,
        output_dir=output_dir,
    )
    for tex_file in TEX_FILES:
        run_pdflatex(tex_file)
        move_outputs(tex_file, result_dir=result_dir)
    print("Build completed successfully")


if __name__ == "__main__":
    main()
