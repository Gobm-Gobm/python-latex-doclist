from pathlib import Path

from drawing_categories import (
    DRAWING_CATEGORY,
    DOCUMENT_CATEGORY,
    CALCULATION_CATEGORY,
    MODEL_CATEGORY,
    PROTOCOL_CATEGORY,
)

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
# Code extraction
# ---------------------------------------------------------------------------

def get_drawing_code(filename: str) -> str:
    """
    Extract drawing / document / model / protocol code.

    Returns:
    - '1103', 'D000', 'C110', 'M100', 'P110'
    - 'N/A' if invalid
    """
    code = _extract_code_block(filename)

    # Numeric drawing code (DDTT)
    if len(code) == 4 and code.isdigit():
        return code

    # Alphanumeric code (D000, C110, M100, P110)
    if len(code) == 4 and code[0].isalpha() and code[1:].isdigit():
        return code

    return "N/A"


def get_category_code(filename: str) -> str:
    """
    Extract numeric drawing category (DD).

    Returns:
    - '11', '12', etc.
    - 'N/A' for non-numeric codes
    """
    code = get_drawing_code(filename)

    if code.isdigit():
        return code[:2]

    return "N/A"


# ---------------------------------------------------------------------------
# Drawing category metadata helpers
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
# Alphanumeric category lookup
# ---------------------------------------------------------------------------

def _lookup_alpha_category(code: str) -> dict | None:
    """
    Lookup alphanumeric codes (Dxxx, Cxxx, Mxxx, Pxxx).
    """
    prefix = code[0]

    registry = {
        "D": DOCUMENT_CATEGORY,
        "C": CALCULATION_CATEGORY,
        "M": MODEL_CATEGORY,
        "P": PROTOCOL_CATEGORY,
    }.get(prefix)

    if not registry:
        return None

    return registry.get(code)


# ---------------------------------------------------------------------------
# Human-readable description
# ---------------------------------------------------------------------------

def describe_drawing(filename: str) -> str:
    """
    Generate a human-readable description.

    Rules:
    - Element-based numeric drawings → include type
    - Non-element numeric drawings → label only
    - Alphanumeric codes → label + description (if available)
    """
    code = get_drawing_code(filename)
    if code == "N/A":
        return "N/A"

    # ------------------------------------------------------------------
    # Numeric drawing codes (DDTT)
    # ------------------------------------------------------------------
    if code.isdigit():
        category_code = code[:2]
        type_code = code[2:]

        meta = DRAWING_CATEGORY.get(category_code)
        if not meta:
            return "N/A"

        if meta["element_based"]:
            return f"{meta['label']} type {type_code}"

        return meta["label"]

    # ------------------------------------------------------------------
    # Alphanumeric codes (documents, calculations, models, protocols)
    # ------------------------------------------------------------------
    meta = _lookup_alpha_category(code)
    if not meta:
        return "N/A"

    description = meta.get("description")
    if description:
        return f"{meta['label']} - {description}"

    return meta["label"]


# ---------------------------------------------------------------------------
# Tank handling
# ---------------------------------------------------------------------------

def get_tank_number(filename: str) -> str:
    """
    Extract tank number from filename.

    Returns:
    - 'General' for 00
    - '01', '02', etc.
    - 'N/A' if missing or malformed
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
