# ---------------------------------------------------------------------------
# Numeric drawing categories (DDxx)
# ---------------------------------------------------------------------------

DRAWING_CATEGORY = {

    # ------------------------------------------------------------------
    # Wall panels / primary structure
    # ------------------------------------------------------------------

    "10": {
        "label": "Panel general arrangement",
        "element_based": False,
        "description": "Plan layout with panel numbering",
        "packages": {"for_client", "for_manufacture"},
    },

    "11": {
        "label": "Concrete layout",
        "element_based": True,
        "packages": {"for_client", "for_manufacture"},
    },

    "12": {
        "label": "Concrete layout detail",
        "element_based": True,
        "packages": {"for_client", "for_manufacture"},
    },

    "13": {
        "label": "Reinforcement layout",
        "element_based": True,
        "packages": {"for_manufacture"},
    },

    "14": {
        "label": "Reinforcement layout detail",
        "element_based": True,
        "packages": {"for_manufacture"},
    },

    "19": {
        "label": "Drilling areas / general",
        "element_based": True,
        "packages": {"for_manufacture"},
    },

    # ------------------------------------------------------------------
    # Buttresses
    # ------------------------------------------------------------------

    "41": {
        "label": "Buttress concrete layout",
        "element_based": True,
        "packages": {"for_client", "for_manufacture"},
    },

    "42": {
        "label": "Buttress concrete layout detail",
        "element_based": True,
        "packages": {"for_client", "for_manufacture"},
    },

    "43": {
        "label": "Buttress reinforcement layout",
        "element_based": True,
        "packages": {"for_manufacture"},
    },

    "44": {
        "label": "Buttress reinforcement layout detail",
        "element_based": True,
        "packages": {"for_manufacture"},
    },

    # ------------------------------------------------------------------
    # Roof structures
    # ------------------------------------------------------------------

    "60": {
        "label": "Roof layout (legacy)",
        "element_based": False,
        "packages": {"for_client"},
    },

    "61": {
        "label": "Roof concrete layout",
        "element_based": True,
        "packages": {"for_client", "for_manufacture"},
    },

    "62": {
        "label": "Roof concrete layout detail",
        "element_based": True,
        "packages": {"for_client", "for_manufacture"},
    },

    "63": {
        "label": "Roof reinforcement layout",
        "element_based": True,
        "packages": {"for_manufacture"},
    },

    "64": {
        "label": "Roof reinforcement layout detail",
        "element_based": True,
        "packages": {"for_manufacture"},
    },

    "80": {
        "label": "Roof layout (alternative legacy)",
        "element_based": False,
        "packages": {"for_client", "for_manufacture"},
    },

    "81": {
        "label": "Roof concrete layout",
        "element_based": True,
        "packages": {"for_client", "for_manufacture"},
    },

    "82": {
        "label": "Roof concrete layout detail",
        "element_based": True,
        "packages": {"for_client", "for_manufacture"},
    },

    "83": {
        "label": "Roof reinforcement layout",
        "element_based": True,
        "packages": {"for_manufacture"},
    },

    "84": {
        "label": "Roof reinforcement layout detail",
        "element_based": True,
        "packages": {"for_manufacture"},
    },

    # ------------------------------------------------------------------
    # Base, excavation, setting out
    # ------------------------------------------------------------------

    "50": {
        "label": "Setting out / reference",
        "element_based": False,
        "packages": {"for_manufacture"},
    },

    "51": {
        "label": "Excavation",
        "element_based": False,
        "packages": {"for_client", "for_manufacture"},
    },

    "70": {
        "label": "Baseplate relations",
        "element_based": False,
        "description": "Interfaces and relation drawings",
        "packages": {"for_client", "for_manufacture"},
    },

    "71": {
        "label": "Baseplate geometry",
        "element_based": False,
        "packages": {"for_client", "for_manufacture"},
    },

    "72": {
        "label": "Baseplate geometry detail",
        "element_based": False,
        "packages": {"for_manufacture"},
    },

    "73": {
        "label": "Baseplate reinforcement",
        "element_based": False,
        "description": "Base mesh and ring beam stirrups",
        "packages": {"for_manufacture"},
    },

    # ------------------------------------------------------------------
    # Temporary works
    # ------------------------------------------------------------------

    "90": {
        "label": "Temporary works general",
        "element_based": False,
        "packages": {"for_manufacture"},
    },

    "91": {
        "label": "Temporary works concrete layout",
        "element_based": True,
        "packages": {"for_manufacture"},
    },

    "92": {
        "label": "Temporary works detail",
        "element_based": True,
        "packages": {"for_manufacture"},
    },

    "93": {
        "label": "Temporary works reinforcement layout",
        "element_based": True,
        "packages": {"for_manufacture"},
    },

    "94": {
        "label": "Temporary works reinforcement detail",
        "element_based": True,
        "packages": {"for_manufacture"},
    },
}


# ---------------------------------------------------------------------------
# Alphanumeric categories
# ---------------------------------------------------------------------------

DOCUMENT_CATEGORY = {
    "D000": {
        "label": "Drawing list / document register",
        "description": "Index of drawings and documents for the project",
        "packages": {"for_client"},
    },

    "D100": {
        "label": "Design risk assessment",
        "description": "Designer risk assessment and hazard identification",
        "packages": {"for_client"},
    },

    "D110": {
        "label": "User / operator manual",
        "description": "Operation, use, and maintenance instructions",
        "packages": {"for_client"},
    },
}

CALCULATION_CATEGORY = {
    "C100": {
        "label": "Baseplate calculations",
        "description": "Structural design calculations for baseplate",
        "packages": {"for_client", "for_manufacture"},
    },

    "C110": {
        "label": "Wall panel calculations",
        "description": "Structural design calculations for wall panels",
        "packages": {"for_client", "for_manufacture"},
    },

    "C120": {
        "label": "Wall propping calculations",
        "description": "Temporary propping and stability calculations",
        "packages": {"for_manufacture"},
    },

    "C130": {
        "label": "Roof calculations",
        "description": "Structural design calculations for roof elements",
        "packages": {"for_client", "for_manufacture"},
    },

    "C190": {
        "label": "General calculations",
        "description": "General or supporting structural calculations",
        "packages": {"for_client", "for_manufacture"},
    },
}


MODEL_CATEGORY = {
    "M100": {
        "label": "3D model (tank)",
        "description": "Native 3D coordination and reference model",
        "packages": {"for_client", "for_manufacture"},
    },
}


PROTOCOL_CATEGORY = {
    "P100": {
        "label": "Installation / post-tensioning protocol",
        "description": "General installation and post-tensioning procedure",
        "packages": {"for_manufacture"},
    },

    "P110": {
        "label": "Wall panel tensioning protocol",
        "description": "Procedure for stressing wall panel tendons",
        "packages": {"for_manufacture"},
    },

    "P120": {
        "label": "Tendon elongation records",
        "description": "Measured and calculated tendon elongations",
        "packages": {"for_manufacture"},
    },

    "P130": {
        "label": "Stressing sequence documentation",
        "description": "Defined stressing order and sequence",
        "packages": {"for_manufacture"},
    },

    "P190": {
        "label": "Other installation / PT documents",
        "description": "Other installation or post-tensioning records",
        "packages": {"for_manufacture"},
    },
}



# Unified registry for non-numeric codes
CODE_REGISTRY = {}
CODE_REGISTRY.update(DOCUMENT_CATEGORY)
CODE_REGISTRY.update(CALCULATION_CATEGORY)
CODE_REGISTRY.update(MODEL_CATEGORY)
CODE_REGISTRY.update(PROTOCOL_CATEGORY)
