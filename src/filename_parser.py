from pathlib import Path
from drawing_categories import DRAWING_CATEGORY

def category_packages(category_code: str) -> set[str]:
    meta = DRAWING_CATEGORY.get(category_code)
    return meta["packages"] if meta else set()

def category_label(category_code: str) -> str:
    meta = DRAWING_CATEGORY.get(category_code)
    return meta["label"] if meta else "N/A"

def get_category_code(filename: str) -> str:
    code = get_drawing_code(filename)
    if code != "N/A":
        return code[:2]
    return "N/A"


def describe_drawing(filename: str) -> str:
    """
    Generate a human-readable drawing description from filename.

    Example:
    AQ430773-00-45-32-1102.pdf
    → Concrete layout type 02
    """
    stem = Path(filename).stem
    parts = stem.split("-")

    code = parts[-1]

    if len(code) != 4 or not code.isdigit():
        return "N/A"

    category_code = code[:2]
    type_code = code[2:]

    meta = DRAWING_CATEGORY.get(category_code)
    if not meta:
        return "N/A"

    return f"{meta['label']} type {type_code}"

def get_tank_number(filename: str) -> str:
    """
    Extract tank number from filename.

    Expected format:
    AQ430773-01-45-32-1103.pdf

    Returns:
    - "General" for tank 00
    - "01", "02", etc. for specific tanks
    - "N/A" if format is unexpected
    """
    parts = filename.split("-")

    if len(parts) < 2:
        return "N/A"

    tank = parts[1]

    if tank == "00":
        return "General"

    if tank.isdigit():
        return tank

    return "N/A"

def get_drawing_code(filename: str) -> str:
    """
    Extract drawing code from filename.

    Expected format:
    AQ430773-01-45-32-1103.pdf

    Returns:
    - '1103' if present and valid
    - 'N/A' otherwise
    """
    stem = Path(filename).stem
    parts = stem.split("-")

    if not parts:
        return "N/A"

    code = parts[-1]

    if len(code) == 4 and code.isdigit():
        return code

    return "N/A"
