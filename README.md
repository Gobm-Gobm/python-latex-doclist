# Python LaTeX Doc List

Generate LaTeX drawing/document lists and build client, manufacture, and installation report PDFs.

**Quick Start**

1. Add your source files under `data/documents/`.
2. Run the build:

```bash
python3 src/build.py
```

**Outputs**

The build produces:

- `output/document_list_for_client.tex`
- `output/document_list_for_manufacture.tex`
- `output/document_list_for_installation.tex`
- `latex_result/report_for_client.pdf`
- `latex_result/report_for_manufacture.pdf`
- `latex_result/report_for_installation.pdf`

**How Files Are Parsed**

Expected filename pattern:

```
<Project>-<Tank>-<Group>-<Discipline>-<Code>[_Description].ext
```

Examples:

- `AQ430773-00-45-32-1103.pdf`
- `AQ430773-02-45-32-M100_Tank02.rvt`
- `AQ430773-00-45-32-D000_Drawing_list.pdf`

Notes:

- Tank `00` is treated as General.
- Numeric codes are 4 digits (e.g., `1103`).
- Alphanumeric codes are 1 letter + 3 digits (e.g., `D000`, `C110`, `M100`, `P110`).

**Packages**

Package routing is controlled in `src/drawing_categories.py` via the `packages` field.

Current packages:

- `for_client`
- `for_manufacture`
- `for_installation`

**Layout and Styling**

The list layout is generated in `src/generate_doc_list.py`.

- Section headers and row shading are controlled in `write_latex_list()`.
- The LaTeX preamble lives at `tex-templates/setup/report/preamble.tex`.
- Report wrappers live in `latex_build/test/report_for_client.tex`, `latex_build/test/report_for_manufacture.tex`, and `latex_build/test/report_for_installation.tex`.
