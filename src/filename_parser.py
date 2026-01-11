from pathlib import Path

# Mapping of drawing category codes
DRAWING_CATEGORY = {
    "11": "Concrete layout",
    "13": "Reinforcement layout",
}


def describe_drawing(filename: str) -> str:
    """
    Generate a human-readable drawing description from filename.

    Example:
    AQ430773-00-45-32-1102.pdf
    → Concrete layout type 02
    """
    stem = Path(filename).stem
    parts = stem.split("-")

    if not parts:
        return "N/A"

    code = parts[-1]  # last part, e.g. '1102'

    if len(code) != 4 or not code.isdigit():
        return "N/A"

    category_code = code[:2]
    type_code = code[2:]

    category = DRAWING_CATEGORY.get(category_code, "N/A")

    if category == "N/A":
        return "N/A"

    return f"{category} type {type_code}"
