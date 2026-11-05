
from rag.query_builder import build_skin_query
from rag.retrieval import retrieve_information


def build_skin_context(skin_profile):
    """
    Connect a skin profile to the RAG knowledge base.
    Returns measured features and relevant retrieved documents.
    """

    context = {
        "status": "success",
        "zones": {}
    }

    for zone, zone_data in skin_profile.items():

        if zone_data.get("status") != "analyzed":
            context["zones"][zone] = {
                "status": "skipped",
                "reason": "No valid analysis available"
            }
            continue

        features = zone_data.get(
            "features",
            zone_data.get("raw_features", {})
        )

        query = build_skin_query(zone, features)
        results = retrieve_information(query)

        documents = results.get("documents", [[]])[0]

        context["zones"][zone] = {
            "status": "retrieved",
            "features": features,
            "query": query,
            "documents": documents
        }

    return context