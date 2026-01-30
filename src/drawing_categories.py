# Drawing category definitions and package routing

DRAWING_CATEGORY = {

    # ------------------------------------------------------------------
    # Wall panels / primary structure
    # ------------------------------------------------------------------

    "10": {
        "label": "Panel general arrangement",
        "element_based": False,
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
        "element_based": False,
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


DOCUMENT_CATEGORY = {
    "D000": {
        "label": "Drawing list / document register",
        "packages": {"for_client"},
    },

    "D100": {
        "label": "Design risk assessment",
        "packages": {"for_client"},
    },

    "D110": {
        "label": "User / operator manual",
        "packages": {"for_client"},
    },
}
