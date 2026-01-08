from pathlib import Path

DOCUMENTS_DIR = Path("data/documents")
OUTPUT_FILE = Path("output/document_list.tex")
EXTENSIONS = {
    ".pdf",   # reports, drawings
    ".tex",   # source documents
    ".rvt",   # Revit models
}

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

def escape_latex(text: str) -> str:
    for char, replacement in LATEX_SPECIAL_CHARS.items():
        text = text.replace(char, replacement)
    return text

def get_documents(folder: Path):
    return sorted(
        f for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in EXTENSIONS
    )

def write_latex_list(files, output_file: Path):
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as f:
        f.write("% Auto-generated file — do not edit manually\n")
        f.write("\\section*{Document List}\n")
        f.write("\\begin{itemize}\n")

        for file in files:
            safe_name = escape_latex(file.name)
            f.write(f"  \\item {safe_name}\n")

        f.write("\\end{itemize}\n")

def main():
    files = get_documents(DOCUMENTS_DIR)
    write_latex_list(files, OUTPUT_FILE)
    print(f"Wrote {len(files)} documents to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
