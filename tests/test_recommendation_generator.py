
from rag.skin_context import build_skin_context
from rag.llm_input import build_llm_input
from rag.recommendation_generator import generate_recommendations


sample_profile = {
    "forehead": {
        "status": "analyzed",
        "features": {
            "brightness": 153.0,
            "redness": 0.385,
            "color_statistics": {
                "mean_r": 177.6,
                "mean_g": 142.3,
                "mean_b": 143.2
            }
        }
    },
    "left cheek": {
        "status": "missing"
    }
}


def test_recommendation_generator():
    context = build_skin_context(sample_profile)
    llm_input = build_llm_input(context)
    result = generate_recommendations(llm_input)

    assert result["mode"] == "mock"
    assert len(result["zone_results"]) == 1

    forehead = result["zone_results"][0]

    assert forehead["zone"] == "forehead"
    assert len(forehead["evidence_references"]) > 0
    assert len(forehead["suggestions"]) > 0

    assert all(
        suggestion in {
            "Avoid harsh cleansing.",
            "Consider gentle routines that support the skin barrier.",
            "Consider a gentle skincare routine."
        }
        for suggestion in forehead["suggestions"]
    )

    assert all(
        zone["zone"] != "left cheek"
        for zone in result["zone_results"]
    )

    print("Recommendation generator test passed.")
    print(result)


if __name__ == "__main__":
    test_recommendation_generator()
