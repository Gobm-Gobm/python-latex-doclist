from filename_parser import get_drawing_code

CATEGORY_BLOCKS = [
    ("11", "12", "13", "14", "19"),  # Wall panels
    ("41", "42", "43", "44"),  # Buttresses
    ("61", "62", "63", "64"),  # Roof
]

def panel_type_grouped(file):
    """
    Sort order:
    1. Category block (walls → buttresses → roof)
    2. Type code (00, 01, 02, ...)
    3. Category order inside block
    """
    code = get_drawing_code(file.name)

    if not code.isdigit():
        return (999, 999, 999)

    category = code[:2]
    type_code = int(code[2:])

    for block_index, block in enumerate(CATEGORY_BLOCKS):
        if category in block:
            category_index = block.index(category)
            return (block_index, type_code, category_index)

    return (999, type_code, 999)
