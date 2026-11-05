
def generate_recommendations(llm_input):
    """
    Generate cautious, evidence-grounded recommendations.
    This is a deterministic mock, not a real LLM.
    """

    if not isinstance(llm_input, dict):
        raise TypeError("llm_input must be a dictionary")

    evidence = llm_input.get("evidence", [])
    zones = llm_input.get("zones", [])

    results = []

    for zone in zones:
        if zone.get("status") != "analyzed":
            continue

        zone_name = zone["zone"]

        relevant_evidence = [
            item for item in evidence
            if item.get("zone") == zone_name
        ]

        # Only use guidance explicitly present in retrieved evidence.
        recommendations = []

        for item in relevant_evidence:
            text = item.get("text", "").lower()

            if "avoid harsh cleansing" in text:
                recommendations.append(
                    "Avoid harsh cleansing."
                )

            if "support skin barrier" in text:
                recommendations.append(
                    "Consider gentle routines that support the skin barrier."
                )

            if "use gentle skincare routines" in text:
                recommendations.append(
                    "Consider a gentle skincare routine."
                )

        # Remove duplicate suggestions while preserving order.
        recommendations = list(dict.fromkeys(recommendations))

        results.append({
            "zone": zone_name,
            "observations": (
                "Image-derived measurements are available; "
                "they do not establish a medical diagnosis."
            ),
            "suggestions": recommendations,
            "evidence_references": [
                item["evidence_id"]
                for item in relevant_evidence
                if "evidence_id" in item
            ]
        })

    return {
        "mode": "mock",
        "summary": (
            "Suggestions are generated from retrieved knowledge. "
            "This prototype does not provide a medical diagnosis."
        ),
        "zone_results": results,
        "limitations": [
            "This is a deterministic mock, not an LLM.",
            "Image measurements can be affected by lighting and segmentation.",
            "Retrieved knowledge has not been clinically validated."
        ],
        "safety_note": (
            "Seek advice from a qualified healthcare professional "
            "for persistent, worsening, or concerning skin symptoms."
        )
    }
