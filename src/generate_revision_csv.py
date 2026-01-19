from pathlib import Path
import csv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"
CSV_FILE = PROJECT_ROOT / "data" / "revisions.csv"

EXTENSIONS = {".pdf", ".rvt", ".tex"}
DELIMITER = ";"  # Excel-friendly (EU locales)


def get_drawing_ids():
    return {
        f.stem
        for f in DOCUMENTS_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in EXTENSIONS
    }


def read_csv():
    if not CSV_FILE.exists():
        return {}

    with CSV_FILE.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=DELIMITER)
        return {row["drawing_id"]: row for row in reader}


def write_csv(rows):
    fieldnames = ["drawing_id", "rev", "issue_date", "status", "exists"]

    with CSV_FILE.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            delimiter=DELIMITER
        )
        writer.writeheader()
        for row in rows.values():
            writer.writerow(row)


def main():
    file_ids = get_drawing_ids()
    csv_rows = read_csv()

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

    write_csv(csv_rows)
    print("Revision register updated safely.")


if __name__ == "__main__":
    main()
