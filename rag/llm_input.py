import json


def build_llm_input(skin_context):
    """
    Convert retrieved skin context into structured,
    JSON-serializable input for a future LLM.
    """

    if not isinstance(skin_context, dict):
        raise TypeError("skin_context must be a dictionary")

    zones = []
    evidence = []

    for zone, data in skin_context.get("zones", {}).items():
        if data.get("status") != "retrieved":
            zones.append({
                "zone": zone,
                "status": "skipped",
                "reason": data.get(
                    "reason", "No valid analysis or retrieval"
                )
            })
            continue

        features = data.get("features", {})
        if not isinstance(features, dict):
            raise ValueError(
                f"Features for {zone} must be a dictionary"
            )

        zones.append({
            "zone": zone,
            "status": "analyzed",
            "features": features
        })

        for index, document in enumerate(
            data.get("documents", []), start=1
        ):
            evidence.append({
                "evidence_id": f"{zone}_{index}",
                "zone": zone,
                "text": document
            })

    result = {
        "schema_version": "1.0",
        "task": (
            "Generate cautious skincare guidance grounded "
            "in the supplied measurements and retrieved evidence."
        ),
        "safety_constraints": [
            "Do not diagnose medical conditions.",
            "Do not invent measurements or evidence.",
            "Only make claims supported by retrieved evidence.",
            "Treat image-derived measurements as approximate."
        ],
        "zones": zones,
        "evidence": evidence
    }

    # Fail early if the result cannot be serialized to JSON.
    json.dumps(result, allow_nan=False)

    return result
