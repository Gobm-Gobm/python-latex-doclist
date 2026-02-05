import argparse
from pathlib import Path
import csv

PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXTENSIONS = {".pdf", ".rvt", ".tex"}
DELIMITER = ";"  # Excel-friendly (EU locales)


def get_drawing_ids(documents_dir: Path):
    if not documents_dir.exists():
        return set()

    return {
        f.stem.split("_", 1)[0]
        for f in documents_dir.iterdir()
        if f.is_file() and f.suffix.lower() in EXTENSIONS
    }


def read_csv(csv_file: Path):
    if not csv_file.exists():
        return {}

    with csv_file.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=DELIMITER)
        rows = {}
        for row in reader:
            drawing_id = row.get("drawing_id", "").split("_", 1)[0]
            if not drawing_id:
                continue
            row["drawing_id"] = drawing_id
            rows[drawing_id] = row
        return rows


def write_csv(csv_file: Path, rows):
    fieldnames = ["drawing_id", "rev", "issue_date", "status", "exists"]

    csv_file.parent.mkdir(parents=True, exist_ok=True)
    with csv_file.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            delimiter=DELIMITER
        )
        writer.writeheader()
        for row in rows.values():
            writer.writerow(row)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate or update revisions CSV from a documents folder."
    )
    parser.add_argument(
        "--documents-dir",
        type=Path,
        default=PROJECT_ROOT / "data" / "documents",
        help="Folder containing drawing/document files.",
    )
    parser.add_argument(
        "--csv-file",
        type=Path,
        help="Output revisions CSV path. Defaults to <documents-dir>/revisions.csv.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    documents_dir = args.documents_dir.expanduser().resolve()
    csv_file = (
        args.csv_file.expanduser().resolve()
        if args.csv_file is not None
        else (documents_dir / "revisions.csv")
    )

    file_ids = get_drawing_ids(documents_dir)
    csv_rows = read_csv(csv_file)

    # Mark all as not existing initially
    for row in csv_rows.values():
        row["exists"] = "no"

    # Add or update rows based on folder contents
    for drawing_id in file_ids:
        if drawing_id in csv_rows:
            csv_rows[drawing_id]["exists"] = "yes"
        else:
            csv_rows[drawing_id] = {
                "drawing_id": drawing_id,
                "rev": "",
                "issue_date": "",
                "status": "",
                "exists": "yes",
            }

    write_csv(csv_file, csv_rows)
    print(f"Revision register updated safely: {csv_file}")


if __name__ == "__main__":
    main()
