"""
NeuroQ-Flood — Nature-Based Flood Mitigation

Maps flood-risk classifications to
suggested mitigation strategies.
"""

RECOMMENDATIONS = {

    "LOW":
        "Green roofs / permeable surfaces "
        "for routine runoff reduction",

    "MODERATE":
        "Rain gardens and bioswales "
        "to slow and absorb runoff",

    "HIGH":
        "Detention/retention storage plus "
        "expanded green infrastructure",

    "SEVERE":
        "Prioritize flood storage, drainage relief, "
        "and emergency mitigation planning"

}


def recommend(risk):

    return RECOMMENDATIONS[risk]