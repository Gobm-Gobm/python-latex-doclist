from filename_parser import (
    get_drawing_code,
    get_tank_number,
    category_is_element_based,
)

def document_group(file) -> int:
    """
    Assign a logical group number for drawing list presentation.

    Lower number = appears earlier in list.
    """
    if get_tank_number(file.name) != "General":
        return 99  # non-tank-00 handled elsewhere

    code = get_drawing_code(file.name)

    # 1 — Plan views & sections
    if code.isdigit() and code.startswith("10"):
        return 1

    # 2 — Element-based drawings
    if code.isdigit():
        category = code[:2]
        if category_is_element_based(category):
            return 2

    # 3 — Models
    if code.startswith("M"):
        return 3

    # 4 — Docs, calcs, protocols
    if code[0] in {"D", "C", "P"}:
        return 4

    return 99
