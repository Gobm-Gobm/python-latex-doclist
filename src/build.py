import subprocess
import shutil
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Scripts and files
DOC_LIST_SCRIPT = PROJECT_ROOT / "src" / "generate_doc_list.py"
TEX_FILE = PROJECT_ROOT / "latex_build" / "test" / "report.tex"

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

def generate_document_list():
    """
    Generoutputate the LaTeX document list from files in data/documents.
    """
    print("Generating document list...")
    subprocess.run(
        [sys.executable, DOC_LIST_SCRIPT.name],
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


def move_outputs(tex_file: Path):
    """
    Move the generated PDF and LaTeX build artefacts into
    their respective folders.
    """
    RESULT_DIR.mkdir(exist_ok=True)
    BUILD_DIR.mkdir(exist_ok=True)

    base_name = tex_file.stem

    for file in tex_file.parent.iterdir():
        # Final PDF → latex_result/
        if file.suffix == ".pdf" and file.stem == base_name:
            shutil.move(str(file), RESULT_DIR / file.name)

        # Build artefacts → latex_build/
        elif file.suffix in LATEX_EXTENSIONS:
            shutil.move(str(file), BUILD_DIR / file.name)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    generate_document_list()
    run_pdflatex(TEX_FILE)
    move_outputs(TEX_FILE)
    print("Build completed successfully")


if __name__ == "__main__":
    main()
