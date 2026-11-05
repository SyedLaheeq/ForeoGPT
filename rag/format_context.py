
def format_context_for_llm(skin_context):
    """
    Convert retrieved skin context into a compact,
    readable prompt context for a future LLM.
    """

    sections = []

    for zone, data in skin_context.get("zones", {}).items():

        if data.get("status") != "retrieved":
            continue

        sections.append(f"FACIAL ZONE: {zone}")

        sections.append(
            "MEASUREMENTS:\n"
            + str(data.get("features", {}))
        )

        sections.append("RETRIEVED KNOWLEDGE:")

        for index, document in enumerate(
            data.get("documents", []), start=1
        ):
            sections.append(
                f"Source {index}:\n{document}"
            )

    if not sections:
        return "No valid skin measurements or retrieved knowledge available."

    return "\n\n".join(sections)