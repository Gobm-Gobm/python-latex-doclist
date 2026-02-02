from pathlib import Path

from drawing_categories import DRAWING_CATEGORY, CODE_REGISTRY


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------

def _stem_parts(filename: str) -> list[str]:
    """
    Split filename stem into dash-separated parts.

    AQ430773-01-45-32-1103_Concrete_layout.pdf
    -> [..., '1103_Concrete_layout']
    """
    return Path(filename).stem.split("-")


def _extract_code_block(filename: str) -> str:
    """
    Extract the final code block (before optional underscore description).

    Examples:
    - 1103                  -> 1103
    - 1103_Concrete_layout  -> 1103
    - D000_Drawing_list     -> D000
    """
    parts = _stem_parts(filename)
    if not parts:
        return "N/A"

    raw = parts[-1]
    return raw.split("_")[0]


# ---------------------------------------------------------------------------
# Drawing / document code extraction
# ---------------------------------------------------------------------------

def get_drawing_code(filename: str) -> str:
    """
    Extract drawing / document / model / protocol code.

    Returns:
    - '1103', 'D000', 'C110', 'M100', 'P110'
    - 'N/A' if invalid
    """
    code = _extract_code_block(filename)

    # Numeric drawing code: 4 digits
    if len(code) == 4 and code.isdigit():
        return code

    # Alphanumeric code: 1 letter + 3 digits (D000, C110, M100, P110)
    if len(code) == 4 and code[0].isalpha() and code[1:].isdigit():
        return code.upper()

    return "N/A"


def get_category_code(filename: str) -> str:
    """
    Extract numeric drawing category (DD) for numeric drawing codes only.

    Returns:
    - '11', '12', etc.
    - 'N/A' for non-numeric codes
    """
    code = get_drawing_code(filename)
    if code.isdigit():
        return code[:2]
    return "N/A"


# ---------------------------------------------------------------------------
# Category metadata (numeric drawings)
# ---------------------------------------------------------------------------

def category_label(category_code: str) -> str:
    meta = DRAWING_CATEGORY.get(category_code)
    return meta["label"] if meta else "N/A"


def category_packages(category_code: str) -> set[str]:
    meta = DRAWING_CATEGORY.get(category_code)
    return meta["packages"] if meta else set()


def category_is_element_based(category_code: str) -> bool:
    meta = DRAWING_CATEGORY.get(category_code)
    return meta["element_based"] if meta else False


# ---------------------------------------------------------------------------
# Code registry metadata (alphanumeric + routing helper)
# ---------------------------------------------------------------------------

def code_packages(code: str) -> set[str]:
    """
    Return package routing for ANY code.

    - numeric '1103' -> uses DRAWING_CATEGORY on '11'
    - alphanumeric 'D000' -> uses CODE_REGISTRY lookup
    """
    if code == "N/A":
        return set()

    if code.isdigit():
        return category_packages(code[:2])

    meta = CODE_REGISTRY.get(code)
    return meta["packages"] if meta else set()


def code_label(code: str) -> str:
    if code == "N/A":
        return "N/A"

    if code.isdigit():
        meta = DRAWING_CATEGORY.get(code[:2])
        return meta["label"] if meta else "N/A"

    meta = CODE_REGISTRY.get(code)
    return meta["label"] if meta else "N/A"


def code_description(code: str) -> str:
    """
    Short description (mostly for alphanumeric codes).
    """
    if code == "N/A":
        return "N/A"

    if code.isdigit():
        return ""  # numeric drawings are described via category + type

    meta = CODE_REGISTRY.get(code)
    return meta.get("description", "") if meta else ""


# ---------------------------------------------------------------------------
# Human-readable description
# ---------------------------------------------------------------------------

def describe_drawing(filename: str) -> str:
    """
    Generate a human-readable description.

    Rules:
    - Element-based numeric categories -> include type
    - Non-element-based numeric -> category label only
    - Alphanumeric codes -> label + short description (if available)
    """
    code = get_drawing_code(filename)
    if code == "N/A":
        return "N/A"

    # Numeric drawing code (DDTT)
    if code.isdigit():
        category = code[:2]
        type_code = code[2:]

        meta = DRAWING_CATEGORY.get(category)
        if not meta:
            return "N/A"

        if meta["element_based"]:
            return f"{meta['label']} type {type_code}"

        return meta["label"]

    # Alphanumeric codes (D000, C110, M100, P110)
    meta = CODE_REGISTRY.get(code)
    if not meta:
        return "N/A"

    label = meta.get("label", "N/A")
    desc = meta.get("description", "")

    return f"{label} — {desc}" if desc else label


# ---------------------------------------------------------------------------
# Tank handling
# ---------------------------------------------------------------------------

def get_tank_number(filename: str) -> str:
    """
    Extract tank number.

    Returns:
    - 'General' for 00
    - '01', '02', etc.
    - 'N/A' if missing/unexpected
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
